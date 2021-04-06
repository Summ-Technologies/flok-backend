from hawk_db.auth import UserLoginId
from sqlalchemy.orm import Session, joinedload


def load_user_fn(session: Session):
    """Load user for JWT"""

    def load_user(login_id):
        valid_user_login: UserLoginId = (
            session.query(UserLoginId)
            .filter(UserLoginId.is_active == True)
            .filter(UserLoginId.login_id == login_id)
            .options(joinedload(UserLoginId.user))
            .one_or_none()
        )
        if valid_user_login:
            return valid_user_login.user

    return load_user
