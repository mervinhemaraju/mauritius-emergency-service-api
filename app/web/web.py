import os
from flask import Blueprint, render_template as HTML, request, current_app
from flask_mail import Message, Mail
from validate_email import validate_email

# * Create the web blueprint
web = Blueprint("web", __name__, static_folder="static", template_folder="templates")


# >>>> Main Pages <<<< #
@web.route("/")
def home_view():
    return HTML("index.html")

@web.route("/privacy")
def privacy_view():
    return HTML("privacy.html")
    
@web.route("/send-email", methods=["POST"])
def send_email():

    # > Sends a mail from the contact form
    
    # * Create a mail object
    mail = Mail(current_app)

    try:
        sender_email = request.form["email"]

        # * Email validity check
        if not validate_email(sender_email):
            return (
                "Please enter a valid email",
                200,
            )

        msg = Message(
            request.form["message"],
            sender=(request.form["name"], sender_email),
            recipients=os.environ["MAIL_RECIPIENTS"].split(","),
        )
        msg.body = request.form["message"]
        msg.subject = f"{sender_email} :: {request.form['subject']}"
        mail.send(msg)

    except Exception as e:
        print(e)
        return (
            'Unfortunately, your message couldn\'t be submitted right now. Please contact me directly on <a href="mailto:th3pl4gu33@gmail.com">th3pl4gu33@gmail.com</a>.',
            200,
        )

    # * Returns a no content status code
    # * because the user doesn't need to get away
    # * from current page
    return "OK", 200