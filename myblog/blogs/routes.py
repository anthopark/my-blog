from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from myblog import db
from flask_login import login_user, login_required, current_user
from myblog.models import BlogEntry, User, Tag, entry_tag
from myblog.blogs.forms import BlogPostForm

import myblog.blogs.utils as utils

blogs = Blueprint('blogs', __name__)


@blogs.route("/blogs")
def blog_page():
    page = request.args.get('page', 1, type=int)

    entries = BlogEntry.query.filter_by(
        is_published=True).order_by(
        BlogEntry.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template("blogs.html", entries=entries, title="Blogs")


@blogs.route("/blogs/tags")
def tag_list():
    tag_freq_list = utils.get_tag_frequency_list()

    return render_template("tags.html", title="Blog Tags", tag_freqs=tag_freq_list)


@blogs.route("/blogs/tags/<tag>")
def by_tag(tag):
    page = request.args.get('page', 1, type=int)

    entries = BlogEntry.query.filter(BlogEntry.tags.any(
        Tag.name == tag.title())).order_by(
        BlogEntry.date_posted.desc()).paginate(page=1, per_page=5)

    return render_template("blogs.html", entries=entries,
                           title=f"Blogs - {tag.title()}", tag_name=tag)


@blogs.route("/post-new", methods=['GET', 'POST'])
@login_required
def post_entry():
    form = BlogPostForm()
    if form.validate_on_submit():

        new_entry = utils.create_blog_entry(form)

        utils.handle_tags(new_entry, utils.split_tags(form.tags.data))

        flash('New blog post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template("post-entry.html",
                           title="Post New Blog", form=form, legend="Post New Blog")


@blogs.route("/blog/<slug>")
def single_entry(slug):
    entry = BlogEntry.query.filter_by(slug=slug).first()
    if not entry:
        abort(404)
    if not entry.is_published:
        abort(403)

    return render_template('single-entry.html', title=entry.title, entry=entry)


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

        utils.update_blog_entry(entry, form)

        flash('Your post has been updated!', 'success')
        return redirect(url_for('blogs.single_entry', slug=entry.slug))
    elif request.method == 'GET':
        form.title.data = entry.title
        form.content.data = entry.content
        form.tags.data = ", ".join([t.name for t in entry.tags])

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
    flash(
        f"{entry.title if len(entry.title) <= 30 else entry.title[:30] + '...'} Unpublished!", 'info')

    return redirect(url_for('main.home'))
