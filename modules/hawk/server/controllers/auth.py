from typing import Any, Dict

from flask_restful import Resource
from hawk_auth.auth_manager import AuthManager
from hawk_models.auth import FlokLoginData, UserLoginProviderType
from hawk_models.user import UserApiModelSchema
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
        logged_in_user = auth_manager.signin_user(
            login_provider=args["login_provider"],
            login_provider_uid=args["email"],
            login_provider_data=FlokLoginData(password=args["password"]),
        )
        user_login_id = auth_manager.user_login_id(logged_in_user)
        auth_manager.commit_changes()
        return responses.success(
            {"user": UserApiModelSchema.dump(obj=logged_in_user)},
            extra_headers=web.login_cookie_header(jwt, user_login_id.login_id),
        )


class AuthSignupController(Resource):
    post_args = {
        "email": fields.Email(required=True),
        "password": fields.String(required=True),
        "login_provider": fields.Function(
            data_key="loginProvider",
            deserialize=lambda lp: UserLoginProviderType[lp],
            required=True,
        ),
        "first_name": fields.String(
            data_key="firstName",
        ),
        "last_name": fields.String(
            data_key="lastName",
        ),
    }

    @use_args(post_args, location="json")
    def post(self, args: Dict[str, Any]):
        new_user = auth_manager.signup_user(
            args["email"],
            login_provider=args["login_provider"],
            login_provider_uid=args["email"],
            login_provider_data=FlokLoginData(password=args["password"]),
            first_name=args.get("first_name"),
            last_name=args.get("last_name"),
        )
        user_login_id = auth_manager.user_login_id(new_user)
        auth_manager.commit_changes()
        return responses.success(
            {"user": UserApiModelSchema.dump(obj=new_user)},
            extra_headers=web.login_cookie_header(jwt, user_login_id.login_id),
        )