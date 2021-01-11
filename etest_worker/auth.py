import requests
from html.parser import HTMLParser
from typing import Optional

from . import Config, logger
from .exceptions import AuthenticationError


class LoginTokenParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        self._login_token = None
        super(LoginTokenParser, self).__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        if (
            tag == "input"
            and ("type", "hidden") in attrs
            and ("name", "logintoken") in attrs
        ):
            for key, value in attrs:
                if key == "value":
                    self._login_token = value

    def parse(self, data: str) -> Optional[str]:
        self._login_token = None
        super(LoginTokenParser, self).feed(data)
        return self._login_token

    def error(self, message):
        pass


login_token_parser = LoginTokenParser()


def _get_login_token(session: requests.Session) -> str:
    login_request = session.get(Config.LOGIN_URL, timeout=Config.TIMEOUT)
    login_token: Optional[str] = login_token_parser.parse(login_request.text)
    if login_token is None:
        msg = "Cannot parse login token from ETest"
        logger.error(msg)
        raise AuthenticationError(msg)
    return login_token


def auth_user(
    login: str, password: str, close_session: bool = True
) -> Optional[requests.Session]:
    session = requests.session()

    logger.info("Attempt to authenticate user: %s", login)
    login_token = _get_login_token(session)
    auth_requests = session.post(
        Config.LOGIN_URL,
        data={
            "username": login,
            "password": password,
            "logintoken": login_token,
            "anchor": "",
        },
        timeout=Config.TIMEOUT,
    )

    if auth_requests.url == Config.LOGIN_URL:
        raise AuthenticationError("Invalid login or password for ETest")
    if not close_session:
        return session
    session.close()
