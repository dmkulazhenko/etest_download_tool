from enum import Enum
from functools import wraps
from typing import Callable, Any

from flask import current_app, flash, redirect, url_for
from flask_login import current_user


class FlashMessage(dict):
    class Color(str, Enum):
        RED = "danger"
        YELLOW = "warning"
        GREEN = "success"
        BLUE = "info"

    def __init__(self, color: Color, msg: str):
        self.color = color
        self.msg = msg
        super().__init__(color=color, msg=msg)


def anonymous_user(redirect_url: str = "main.index") -> Callable:
    """
    Decorator which redirects client to redirect_url,
    if client is authenticated.
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs) -> Any:
            if current_user.is_authenticated:
                current_app.logger.warning(
                    "User %s tried to access %s", current_user, f
                )
                flash(
                    FlashMessage(
                        FlashMessage.Color.YELLOW, "You are already authorized"
                    )
                )
                return redirect(url_for(redirect_url))
            return f(*args, **kwargs)

        return wrapper

    return decorator
