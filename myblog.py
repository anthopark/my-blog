from flask import Flask, render_template, url_for
from forms import BlogPostForm, ContactForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '12c65ff986cfb670141e121a406c9f60'

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


@app.route("/contact")
def contact():
    form = ContactForm()
    return render_template("contact.html", title="Contact", form=form)



@app.route("/post-entry")
def post_entry():
    form = BlogPostForm()
    return render_template("post-entry.html", title="Post Blog Entry", form=form)



if __name__ == "__main__":
    app.run(debug=True) 