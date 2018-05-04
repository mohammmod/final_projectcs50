import csv
import urllib.request
import datetime


from flask import redirect, render_template, request, session
from functools import wraps


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def check_time(year):

    date = []
    date = year.split("-")
    now = datetime.datetime.now()

    if int(date[0]) < int(now.year) or int(date[0]) > (int(now.year)+2):
        return False

    if int(date[0]) > int(now.year):
        return True

    if int(date[1]) < int(now.month):
        return False

    if int(date[1]) > int(now.month):
        return True

    if int(date[2])<int(now.day):
        return False

    if int(date[2])>int(now.day):
        return True
    return True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


