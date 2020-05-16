from flask import Flask, render_template, url_for, flash, redirect
from forms import BlogPostForm, ContactForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '12c65ff986cfb670141e121a406c9f60'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class BlogEntry(db.Model):

    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    # url friendly version of title
    slug = db.Column(db.String(200), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"BlogEntry('{self.title}', '{self.date_posted}')"






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


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)


@app.route("/post-entry")
def post_entry():
    form = BlogPostForm()
    return render_template("post-entry.html", title="Post Blog Entry", form=form)


if __name__ == "__main__":
    app.run(debug=True)
