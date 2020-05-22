from flask import Blueprint, redirect, flash, url_for, request, render_template
from myblog import bcrypt
from flask_login import login_user, current_user, logout_user
from myblog.models import User
from myblog.admin.forms import LoginForm

admin = Blueprint('admin', __name__)


@admin.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Already logged in!", "info")
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login Successful!", "success")

            # route to the page intented to visit
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful. Please check email and password", 'danger')

    return render_template('login.html', title="Login", form=form)


@admin.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
