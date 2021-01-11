from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    request,
)
from flask_login import login_user, current_user, logout_user
from werkzeug.urls import url_parse

from etest_download.models import User
from etest_download.utils import FlashMessage, anonymous_user
from etest_worker.auth import auth_user
from etest_worker.exceptions import AuthenticationError

from . import bp
from .forms import LoginForm


@bp.route("/login", methods=["GET", "POST"])
@anonymous_user()
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()

        if user is None:
            try:
                auth_user(form.login.data, form.password.data)
            except AuthenticationError as exc:
                current_app.logger.info(
                    "Unsuccessful auth: %s", form.login.data
                )
                flash(FlashMessage(FlashMessage.Color.RED, str(exc)))
                return redirect(url_for("auth.login"))

            user = User(login=form.login.data, password=form.password.data)
            user.commit_to_db()
            current_app.logger.info("New user registered: %s", user)
            flash(
                FlashMessage(
                    FlashMessage.Color.GREEN, "Successfully registered"
                )
            )
        else:
            if form.password.data != user.password:
                flash(
                    FlashMessage(
                        FlashMessage.Color.RED,
                        "Invalid password. "
                        "If you changed your etest password"
                        " – authorize using old password and change it."
                    )
                )
                return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        flash(FlashMessage(FlashMessage.Color.GREEN, "Successfully logged in"))
        current_app.logger.info("User %s logged in", user)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)

    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    current_app.logger.info("User %s logged out", current_user)
    logout_user()
    flash(FlashMessage(FlashMessage.Color.BLUE, "Successfully logged out"))
    return redirect(url_for("auth.login"))
