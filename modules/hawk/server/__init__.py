import summ_logging
import summ_web

from .web import err_code_to_status_code, load_user_fn

app = summ_web.create_app(__name__)
summ_logging.configure_logging(app.config, debug=app.config.get("DEBUG", False))
summ_web.setup_cors(app)
db = summ_web.create_db(app)
api = summ_web.create_api(app)
# rmq: summ_web.FlaskRMQ = summ_web.create_rmq(app)
summ_web.setup_webargs()
jwt = summ_web.create_jwt(app)
jwt.load_user = load_user_fn(session=db.session)
summ_web.setup_exception_handling(api, err_code_to_status_code)

from . import routes

routes.add_routes(api)
