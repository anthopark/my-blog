from myblog import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from myblog.models import BlogEntry, User
from myblog.forms import BlogPostForm, ContactForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Anthony Park',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Anthony Park',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(f"Thank you for reaching out, {form.name.data}!", 'success')
        return redirect(url_for('home'))
    return render_template("contact.html", title="Contact", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Already logged in!", "info")
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login Successful!", "success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check email and password", 'danger')

    return render_template('login.html', title="Login", form=form)


@app.route("/post-entry")
@login_required
def post_entry():
    form = BlogPostForm()
    return render_template("post-entry.html", title="Post Blog Entry", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))