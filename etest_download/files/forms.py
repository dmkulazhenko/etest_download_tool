from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, URL, Length, Optional


from etest_download.models.file import FileType


class AddFileForm(FlaskForm):
    name = StringField("Name", validators=[Optional(), Length(max=256)])
    url = StringField(
        "URL", validators=[DataRequired(), URL(), Length(max=2048)]
    )
    type = RadioField(
        "File type",
        coerce=int,
        choices=[(FileType.presentation.value, "Presentation")],
        validators=[DataRequired(message="Choose file type")],
    )
    submit = SubmitField("Add as PDF")

    def get_type(self) -> FileType:
        return FileType(self.type.data)
