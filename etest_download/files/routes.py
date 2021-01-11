from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory
from flask_login import login_required, current_user

from etest_download.transformer import transformer_classes
from etest_worker.auth import auth_user
from etest_worker.downloader import get_presentation
from etest_worker.exceptions import (
    PresentationParsingError,
    AuthenticationError,
)

from . import bp
from .forms import AddFileForm
from ..models import File
from ..utils import FlashMessage


@bp.route("/files_list", methods=["GET", "POST"])
@login_required
def files_list():
    def return_error(exception: Exception):
        flash(
            FlashMessage(
                FlashMessage.Color.RED,
                "Cannot parse presentation: {}".format(exception),
            )
        )
        return redirect(url_for("files.files_list"))

    form = AddFileForm()

    if form.validate_on_submit():
        try:
            etest_session = auth_user(
                current_user.login, current_user.password, close_session=False
            )
        except AuthenticationError as exc:
            return return_error(exc)

        try:
            slides, sha256 = get_presentation(form.url.data, etest_session)
        except PresentationParsingError as exc:
            return return_error(exc)
        finally:
            etest_session.close()

        file = File(
            name=form.name.data or None,
            orig_url=form.url.data,
            owner_id=current_user.id,
            sha256_hash=sha256,
            type=form.get_type(),
        )
        if file.name is None:
            file.name = str(file.id)

        if file.is_unique_hash:
            transformer_cls = transformer_classes[form.get_type()]
            data = transformer_cls.transform(slides)
            file.file_path.write_bytes(data.read())
        file.commit_to_db()
        current_app.logger.info(
            "User %s added file %s", current_user, file
        )

        return redirect(url_for("files.files_list"))

    return render_template(
        "files/files_list.html",
        title="Files",
        form=form,
        files=current_user.files,
    )


@bp.route("/file/<file_name>")
def get_file(file_name):
    return send_from_directory(current_app.config["FILES_DIR"], file_name)
