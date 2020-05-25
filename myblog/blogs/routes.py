from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from myblog import db
from flask_login import login_user, login_required, current_user
from myblog.models import BlogEntry, User
from myblog.blogs.utils import get_url_slug
from myblog.blogs.forms import BlogPostForm


blogs = Blueprint('blogs', __name__)


@blogs.route("/blogs")
def blog_page():
    page = request.args.get('page', 1, type=int)

    entries = BlogEntry.query.filter_by(
        is_published=True).paginate(page=page, per_page=5)

    return render_template("blogs.html", entries=entries)


@blogs.route("/post-new", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template("post-entry.html",
                           title="Post New Blog", form=form, legend="Post New Blog")


@blogs.route("/blog/<slug>")
def blog_entry(slug):
    entry = BlogEntry.query.filter_by(slug=slug).first()
    if not entry:
        abort(404)

    return render_template('single-entry.html', title=entry.title, entry=entry) \
        if entry else redirect('errors.error_404')


@blogs.route("/blog/<slug>/update", methods=['GET', 'POST'])
@login_required
def update_entry(slug):
    entry = BlogEntry.query.filter_by(slug=slug).first()
    if not entry:
        abort(404)
    if entry.author != current_user:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        # updating the content
        entry.title = form.title.data
        entry.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('blogs.blog_entry', slug=entry.slug))
    elif request.method == 'GET':
        form.title.data = entry.title
        form.content.data = entry.content

    return render_template("post-entry.html",
                           title="Update Blog Post", form=form, legend="Update Blog Post")


@blogs.route("/blog/<slug>/unpublish")
@login_required
def unpublish_entry(slug):
    entry = BlogEntry.query.filter_by(slug=slug).first()
    if not entry:
        abort(404)
    if entry.author != current_user:
        abort(403)

    entry.is_published = False
    db.session.commit()
    flash(f"{entry.title if len(entry.title) <= 30 else entry.title[:30] + '...'} Unpublished!", 'info')

    return redirect(url_for('main.home'))
