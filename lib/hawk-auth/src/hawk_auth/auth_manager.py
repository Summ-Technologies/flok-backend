from typing import Optional, Tuple

import bcrypt
from hawk_db.auth import UserLoginId, UserLoginProvider
from hawk_db.user import User
from hawk_models.auth import (
    FlokLoginData,
    LoginDataABC,
    UserLoginProviderType,
    get_login_data_serializer,
)

from .base_manager import BaseManager
from .exceptions import HawkAuthException


class AuthManager(BaseManager):

    PW_SALT = bcrypt.gensalt(rounds=12)

    def signin_user(
        self,
        login_provider: UserLoginProviderType,
        login_provider_uid: str,
        login_provider_data: LoginDataABC = None,
    ) -> User:
        """Returns user when sign in is successful

        Args:
            login_provider (UserLoginProviderType): what login channel
            login_provider_uid (str): login provider username, often same as email
            login_provider_data (Optional[dict], optional): Includes information for authentication (like password). Defaults to None.

        Raises:
            HawkAuthException: when account doesn't exist or credentials invalid

        Returns:
            User: [description]
        """
        user_login_provider: UserLoginProvider = (
            self.session.query(UserLoginProvider)
            .filter(UserLoginProvider.provider == login_provider.value)
            .filter(UserLoginProvider.unique_id == login_provider_uid)
            .one_or_none()
        )
        if user_login_provider is not None:
            login_data_serializer = get_login_data_serializer(
                UserLoginProviderType[user_login_provider.provider]
            )
            if self._validate_login_data(
                login_provider,
                login_provider_data,
                login_data_serializer.load(user_login_provider.data),
            ):
                return self.session.query(User).get(user_login_provider.user_id)
            else:
                raise HawkAuthException(1003)
        else:
            raise HawkAuthException(1001)

    def signup_user(
        self,
        email: str,
        login_provider: UserLoginProviderType,
        login_provider_uid: str,
        login_provider_data: Optional[LoginDataABC] = None,
        first_name: str = None,
        last_name: str = None,
    ) -> User:
        """Returns new user signup if successful.

        Args:
            email (str)
            login_provider (UserLoginProviderType): what login channel
            login_provider_uid (str): login provider username, often same as email
            login_provider_data (Optional[dict], optional): Includes information for authentication (like password). Defaults to None.
            first_name (str, optional): Defaults to None.
            last_name (str, optional): Defaults to None.

        Raises:
            HawkAuthException: when account exists, login id exists, or credentials aren't valid

        Returns:
            User: Newly signed up User
        """
        if (
            self.session.query(User).filter(User.email == email).one_or_none() is None
            and (
                self.session.query(UserLoginProvider)
                .filter(UserLoginProvider.provider == login_provider.value)
                .filter(UserLoginProvider.unique_id == login_provider_uid)
            ).first()
            is None
        ):
            new_user = User()
            new_user.email = email
            new_user.first_name = first_name
            new_user.last_name = last_name
            self.session.add(new_user)
            self.session.flush()

            new_login = UserLoginProvider()
            new_login.provider = login_provider.value
            new_login.unique_id = login_provider_uid
            new_login.user_id = new_user.id
            new_login.data = self._save_login_data(login_provider, login_provider_data)
            self.session.add(new_login)
            self.session.flush()
            return new_user
        else:
            raise HawkAuthException(1002)

    def user_login_id(self, user: User) -> UserLoginId:
        """Returns UserLoginId record for user (creates one if doesn't exist)"""
        login_id = (
            self.session.query(UserLoginId)
            .filter(UserLoginId.is_active == True)
            .filter(UserLoginId.user_id == user.id)
            .first()
        )
        if login_id:
            return login_id
        else:
            new_login_id = UserLoginId()
            new_login_id.user_id = user.id
            new_login_id.is_active = True
            self.session.add(new_login_id)
            self.session.flush()
            return new_login_id

    def _encrypt_pw(self, password: str) -> str:
        """Generate salted password hash"""
        hashed = bcrypt.hashpw(str(password).encode("utf-8"), self.PW_SALT)
        return hashed.decode("utf-8")

    def _check_pw(self, password: str, password_hash: str) -> bool:
        """Check that password and password_hash match"""
        _password = password.encode("utf-8")
        _password_hash = password_hash.encode("utf-8")
        return bcrypt.checkpw(_password, _password_hash)

    ### Allows for different validation behavior for different login providers
    def _validate_login_data(
        self,
        login_provider: UserLoginProviderType,
        login_provider_data: LoginDataABC,
        saved_login_provider_data: LoginDataABC,
    ) -> bool:
        """Returns (valid)
        valid -> is login valid
            (aka does login_provider_data sufficiently match saved_login_provider_data)
        """
        if login_provider == UserLoginProviderType.FLOK:
            login_data: FlokLoginData = login_provider_data
            saved_login_data: FlokLoginData = saved_login_provider_data
            if self._check_pw(login_data.password, saved_login_data.password):
                return True
            else:
                return False
        else:
            return False

    ### Allows for different validation behavior for different login providers
    def _save_login_data(
        self,
        login_provider: UserLoginProviderType,
        login_provider_data: Optional[LoginDataABC],
    ) -> dict:
        """
        Returns
            data -> data dict to be saved
        Throws
            HawkAuthException when unknown LoginProvider
        """
        if login_provider == UserLoginProviderType.FLOK:
            login_data_serializer = get_login_data_serializer(login_provider)
            plaintext_login_data: FlokLoginData = login_provider_data
            encrypted_pw = self._encrypt_pw(plaintext_login_data.password)
            encrypted_login_data = FlokLoginData(password=encrypted_pw)
            return login_data_serializer.dump(encrypted_login_data)
        else:
            raise HawkAuthException(
                1000,
                f"Can't save login data for unkown login provider: {login_provider}",
            )
