from myblog import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from myblog.models import BlogEntry, User
from myblog.forms import BlogPostForm, ContactForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

from myblog.myutils import get_url_slug


@app.route("/")
@app.route("/home")
def home():
    entries = BlogEntry.query.all()
    return render_template("home.html", entries=entries)


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

            # route to the page intented to visit
            next_page = request.args.get('next')
           
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check email and password", 'danger')

    return render_template('login.html', title="Login", form=form)


@app.route("/post-new", methods=['GET', 'POST'])
@login_required
def post_entry():
    form = BlogPostForm()
    if form.validate_on_submit():

        post = BlogEntry(title=form.title.data,
                         slug=get_url_slug(form.title.data),
                         content=form.content.data,
                         author=current_user)

        db.session.add(post)
        db.session.commit()

        flash('New blog post has been created', 'success')
        return redirect(url_for('home'))
    return render_template("post-entry.html",
                           title="Post New Blog", form=form, legend="Post New Blog")


@app.route("/blog/<slug>")
def blog_entry(slug):
    entry = BlogEntry.query.filter_by(slug=slug).first()

    return render_template('single-entry.html', title=entry.title, entry=entry) \
        if entry else redirect('page_not_found')


@app.route("/blog/<slug>/update", methods=['GET', 'POST'])
@login_required
def update_entry(slug):
    entry = BlogEntry.query.filter_by(slug=slug).first()
    if entry.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        # updating the content
        entry.title = form.title.data
        entry.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('blog_entry', slug=entry.slug))
    elif request.method == 'GET':
        form.title.data = entry.title
        form.content.data = entry.content

    return render_template("post-entry.html",
                           title="Update Blog Post", form=form, legend="Update Blog Post")

@app.route("/blog/<slug>/unpublish")
@login_required
def unpublish_entry(slug):
    entry = BlogEntry.query.filter_by(slug=slug).first()
    if entry.author != current_user:
        abort(403)
    entry.is_published = False
    db.session.commit()
    flash(f"{entry.title[:20]}... Unpublished!", 'info')
    
    return redirect(url_for('home'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/404")
def page_not_found():
    return render_template('404.html', title='Page Not Found')
