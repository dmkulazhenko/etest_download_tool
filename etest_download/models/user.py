from typing import Optional, Union
from flask_login import UserMixin

from etest_download import db, login_manager
from etest_download.models.base import BaseModel


class User(UserMixin, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    files = db.relationship("File", backref="owner", lazy=True)

    def __repr__(self):
        return "<User {}>".format(self.login)


@login_manager.user_loader
def _load_user(uid: Union[str, int]) -> Optional[User]:
    return User.query.get(int(uid))
