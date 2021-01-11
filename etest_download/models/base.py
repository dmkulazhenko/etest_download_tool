from etest_download import db


class BaseModel(db.Model):
    __abstract__ = True

    def commit_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
