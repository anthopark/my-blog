from myblog import mail
from flask_mail import Message
from flask import current_app



def send_email_to_myself(form):
    
    print(current_app.config['MAIL_USERNAME'])
    msg = Message(
        subject=f"Contact From {form.name.data} - My Blog",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[current_app.config['MAIL_USERNAME']],
        body=f"From {form.name.data}({form.email.data})\n\n{form.message.data}" 
    )

    mail.send(msg)