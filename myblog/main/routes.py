from flask import Blueprint, render_template, redirect, flash, url_for
from myblog.models import BlogEntry
from myblog.main.forms import ContactForm
import myblog.main.utils as utils


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # top 5 most recent entries to display
    entries = BlogEntry.query.filter_by(is_published=True).order_by(
        BlogEntry.date_posted.desc()).limit(5).all()

    return render_template("home.html", entries=entries)


@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():

        try:
            utils.send_email_to_myself(form)
        except Exception as e:
            print(e)
            flash(f"Oops, Something went wrong. Please try again!", 'danger')
            return redirect(url_for('main.home'))
        else:
            flash(f"Thank you for reaching out, {form.name.data}!", 'success')
            return redirect(url_for('main.home'))
    return render_template("contact.html", title="Contact", form=form)
