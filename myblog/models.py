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


def slugify(entry_title):
    return entry_title.replace(' ', '-').lower()


entry_tag = db.Table(
    'entry_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('blog_entry.id'))
)


class BlogEntry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    # url friendly version of title
    slug = db.Column(db.String(200), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow,
                             onupdate=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    tags = db.relationship('Tag', secondary=entry_tag,
                           backref='entries', lazy='dynamic')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.slug = slugify(self.title)

    def __repr__(self):
        return f"BlogEntry('{self.title}', '{self.date_posted}')"

    @property
    def markdown_content(self):
        '''
        Convert markdown content into html
        '''

        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()

        markdown_content = markdown(self.content, extensions=[hilite, extras])

        return Markup(markdown_content)

    @property
    def preview_content(self):
        '''
        grab the first image and first two paragraphs of a markdown content 
        '''
        soup = BeautifulSoup(self.markdown_content, 'html.parser')
        return [Markup(p) for p in soup.find_all('p')[:2]]


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return f"Tag('{self.name}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    blog_entries = db.relationship('BlogEntry', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.email}')"
