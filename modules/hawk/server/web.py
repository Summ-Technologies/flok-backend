from typing import Optional

from hawk_db.auth import UserLoginId
from sqlalchemy.orm import Session, joinedload
from summ_web.jwt_auth import JWTManager

### Exception error codes
err_code_to_status_code = {
    1001: 404,
    1002: 422,
    1003: 422,
    1005: 401,
}


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


def login_cookie_header(jwt_manager: JWTManager, login_id: Optional[str]) -> dict:
    """Get set cookie header for user login. If login_id is None, replaces cookie with a null value"""
    token = jwt_manager.encode_jwt(login_id) if login_id else ""
    expires = "315360000"  # ten years in seconds
    return {
        "Set-Cookie": f"{jwt_manager.jwt_cookie_name}={token}; Path=/; Max-Age={expires}; HttpOnly"
    }
