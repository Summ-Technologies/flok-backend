import base64
import os
from logging import getLogger
from typing import Optional

import summ_common
from requests import Session
from requests.models import HTTPError, Response

logger = getLogger(__name__)


class SabreSession(Session):
    def __init__(self) -> None:
        super().__init__()
        self.headers.update({"Accept": "application/json"})

    def request(self, method: str, url: str, **kwargs) -> Response:
        """Extends method found at request.sessions.Session.request"""
        logger.error("HEADERS")
        logger.error(self.headers)
        resp = super().request(method, url, **kwargs)
        try:
            resp.raise_for_status()
        except HTTPError as http_error:
            logger.error(
                "%s %s failed with status_code=%i, response-content=%s",
                method,
                url,
                resp.status_code,
                resp.content.decode("utf-8"),
                exc_info=http_error,
            )
            raise summ_common.exceptions.SummException(
                resp.status_code,
                f"Something went wrong with the request, status_code={resp.status_code}",
            )
        return resp


class SabreClient(object):

    # constants
    AUTH_BASE_URL = "https://api-crt.cert.havail.sabre.com"
    API_BASE_URL = "https://api-crt.cert.havail.sabre.com"

    session: SabreSession
    access_token_basic_auth: Optional[str] = None
    authenticated: bool = False

    def __init__(self, client_id: str, client_secret: str):
        assert client_secret and client_id, "Missing required params"
        self.client_id = client_id
        self.access_token_basic_auth = self._get_b64_auth(client_id, client_secret)

        ## Setup session
        self.session = SabreSession()

        ### TODO REMOVE THIS
        if os.environ.get("SABRE_ACCESS_TOKEN"):
            self.session.headers.update(
                {
                    "Authorization": f"Bearer {os.environ['SABRE_ACCESS_TOKEN']}",
                }
            )
            self.authenticated = True

    def _authenticate(self, force: bool = False) -> None:
        """
        Authenticate with sabre credentials.
        By default, will assume if access_token_basic_auth is set, the session is
            authenticated.
        Args:
            force (bool, optional): Force reauthentication to refresh
                access_token_basic_auth.
                Defaults to False.
        """
        if self.authenticated and not force:
            logger.debug("Already authenticated, not requerying token.")

        else:
            auth_response: Response = self.session.post(
                self._get_url("v2/auth/token"),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {self.access_token_basic_auth}",
                },
                data={"grant_type": "client_credentials"},
            )

            auth_response_json = auth_response.json()
            if auth_response.status_code == 200 and auth_response_json.get(
                "access_token"
            ):
                self.session.headers.update(
                    {
                        "Authorization": f"Bearer {auth_response_json['access_token']}",
                        # "Application-ID": self.client_id,
                    }
                )
                self.authenticated = True
                # TODO REMOVE LOG STATEMENT
                logger.error("Auth Response: %s", auth_response_json)

    ## Utils
    def _get_b64_auth(self, client_id: str, client_secret: str) -> str:
        client_id_b64 = base64.b64encode(client_id.encode("ascii"))
        client_secret_b64 = base64.b64encode(client_secret.encode("ascii"))
        return base64.b64encode(
            f"{client_id_b64.decode('utf-8')}:{client_secret_b64.decode('utf-8')}".encode(
                "ascii"
            )
        ).decode("utf-8")

    def _get_url(self, name: str, **kwargs) -> str:
        """
        Returns full url for given name and args
        """
        urls = {
            "v2/auth/token": self.AUTH_BASE_URL + "/v2/auth/token",
            "v1/shop/flights": self.API_BASE_URL + "/v1/shop/flights",
            "v1/shop/tags/:id": self.API_BASE_URL + "/v1/shop/flights/tags/{id}",
            "themes": self.API_BASE_URL + "/v1/lists/supported/shop/themes/",
        }
        return urls[name].format(**kwargs)

    def get(self, endpoint_name: str, endpoint_args: dict = {}, **kwargs) -> Response:
        """
        See docs for requests.sessions.Session.get
        """
        self._authenticate()
        return self.session.get(self._get_url(endpoint_name, **endpoint_args), **kwargs)

    def post(
        self,
        endpoint_name: str,
        endpoint_args: dict = {},
        data=None,
        json=None,
        **kwargs,
    ) -> Response:
        """
        See docs for requests.sessions.Session.post
        """
        self._authenticate()
        return self.session.post(
            url=self._get_url(endpoint_name, **endpoint_args),
            json=json,
            data=data,
            **kwargs,
        )
