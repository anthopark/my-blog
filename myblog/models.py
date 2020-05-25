from datetime import datetime
from myblog import db, login_manager
from flask_login import UserMixin
from flask import Markup

from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from bs4 import BeautifulSoup

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class BlogEntry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    # url friendly version of title
    slug = db.Column(db.String(200), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_published = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"BlogEntry('{self.title}', '{self.date_posted}')"

    @property
    def markdown_content(self):

        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.content, extensions=[hilite, extras])

        return Markup(markdown_content)

    @property
    def content_preview(self):
        '''
        grab first image and first two paragraphs of a markdown content 
        '''
        soup = BeautifulSoup(self.markdown_content, 'html.parser')
        first_two_p = [str(p) for p in soup.find_all('p')[:2]]
        return Markup(markdown('<br>'.join(first_two_p), extensions=[CodeHiliteExtension(linenums=False, css_class='highlight'), ExtraExtension()]))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    blog_entries = db.relationship('BlogEntry', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.email}')"