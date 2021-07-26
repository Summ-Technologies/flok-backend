from typing import Any, Dict

from flask_restful import Resource
from hawk_auth.auth_manager import AuthManager
from hawk_auth.exceptions import HawkAuthException
from hawk_models.auth import FlokLoginData, UserLoginProviderType
from hawk_models.user import UserSchema
from summ_web import responses
from webargs import fields
from webargs.flaskparser import use_args

from .. import app, db, jwt, web

auth_manager = AuthManager(db.session, app.config)


class AuthSigninController(Resource):
    post_args = {
        "email": fields.Email(required=True),
        "password": fields.String(required=True),
        "login_provider": fields.Function(
            data_key="loginProvider",
            deserialize=lambda lp: UserLoginProviderType[lp],
            required=True,
        ),
    }

    @use_args(post_args, location="json")
    def post(self, args: Dict[str, Any]):
        """POST Login"""
        logged_in_user = auth_manager.signin_user(
            login_provider=args["login_provider"],
            login_provider_uid=args["email"],
            login_provider_data=FlokLoginData(password=args["password"]),
        )
        user_login_id = auth_manager.user_login_id(logged_in_user)
        auth_manager.commit_changes()
        return responses.success(
            {"user": UserSchema().dump(obj=logged_in_user)},
            extra_headers=web.login_cookie_header(jwt, user_login_id.login_id),
        )

    @jwt.requires_auth
    def delete(self):
        """Performs client side logout"""
        return responses.success(
            {"message": "Successfully logged out"},
            extra_headers={
                "Set-Cookie": f"{jwt.jwt_cookie_name}=logged; Path=/; Expires=Mon, 01, Jan 2000, 00:00:00 GMT; HttpOnly"
            },
        )


class AuthResetController(Resource):
    get_args = {
        "login_token": fields.String(required=True),
    }

    @use_args(get_args, location="querystring")
    def get(self, args: Dict[str, any]):
        """Get user for given login_token"""
        user = auth_manager.get_user_by_login_token(login_token=args["login_token"])
        if user:
            return responses.success({"user": UserSchema().dump(obj=user)})
        raise HawkAuthException(1005)

    post_args = {
        "password": fields.String(required=True),
        "login_token": fields.String(required=True),
    }

    @use_args(post_args, location="json")
    def post(self, args: Dict[str, Any]):
        """Update password for given login_token"""
        user = auth_manager.signin_user_and_reset_password(
            user_login_token=args["login_token"],
            login_provider_data=FlokLoginData(password=args["password"]),
            login_provider=UserLoginProviderType.FLOK,
        )
        user_login_id = auth_manager.user_login_id(user)
        auth_manager.commit_changes()
        return responses.success(
            {"user": UserSchema().dump(obj=user)},
            extra_headers=web.login_cookie_header(jwt, user_login_id.login_id),
        )
