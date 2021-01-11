from datetime import datetime
from enum import Enum
from pathlib import Path

from flask import current_app

from etest_download import db
from etest_download.models.base import BaseModel


class FileType(Enum):
    presentation = 1


class File(BaseModel):
    _EXTENSIONS = {
        FileType.presentation: "pdf",
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, nullable=False)
    orig_url = db.Column(db.String(2048), nullable=False)
    sha256_hash = db.Column(db.String(64), nullable=False)
    type = db.Column(db.Enum(FileType), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_time = datetime.utcnow()

    @property
    def file_name(self) -> str:
        return self.sha256_hash + ".{}".format(self._EXTENSIONS[self.type])

    @property
    def file_path(self) -> Path:
        return current_app.config["FILES_DIR"] / self.file_name

    @property
    def is_unique_hash(self) -> bool:
        cnt = File.query.filter(File.sha256_hash == self.sha256_hash).count()
        if self.id is None:  # if self object is not committed to DB
            return cnt < 1
        return cnt < 2

    def __repr__(self):
        return "<File {} owned by {}>".format(self.name, self.owner)
