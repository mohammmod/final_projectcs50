from flask import Flask, flash, redirect, render_template, request, session,send_from_directory, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import apology, login_required,check_time ,allowed_file
from data_base import User_Data
import os
import smtplib
import datetime
from datetime import datetime as dt
from dateutil.parser import parse

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("sportseventsforyou@gmail.com", "ThaerYazen")
msg = "Welcome in Sport Events Webpage"


UPLOAD_FOLDER = 'static'

# Configure application
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
sql_man = User_Data()

@app.route("/",methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("start.html")
    return render_template("mypage.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # make this clean
    # Forget any user_id

    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
       # Ensure username was submitted
        if not username:
             return apology("must provide username", 403)

        # Ensure password was submitted
        if not password:
           return apology("must provide password", 403)

        # # # Query database for username
        rows = sql_man.get_user_info(username)

        # # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
             return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["id"] = rows[0]["id"]

        # Redirect user to home page
        flash("welcome " + username)
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    # User reac hed route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("Missing the E-mail")
        if not request.form.get("username"):
            return apology("Missing the name")

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # submit a empty part without filename
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("not match")

        # Insert the data of the seller
        hash = generate_password_hash(password)
        image = file.filename
        # Insert the data of the new user
        newUser = sql_man.create_user(username, hash, email ,image)
        if not newUser:
            return apology("You are Already registered", 400)

        server.sendmail("sportseventsforyou@gmail.com", email, msg)
        server.quit()

        # Remember which user has logged in
        session["id"] = newUser

        #bring user info and events
        user = sql_man.get_user_infomation(session["id"])
        image = user[0]["image"]
        events = sql_man.get_my_events(session["id"])

        # Redirect user to register page
        flash("Welcome " + username)
        return redirect("/")
     #   return render_template("mypage.html", events=events, image=image)
    else:
        return render_template("register.html")



#@app.route("/start", methods=["GET", "POST"])
#@login_required
#def start():

@app.route("/AboutUs", methods=["GET", "POST"])
def AboutUs():
    """AboutUs"""
    return render_template("AboutUs.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def createvent():
    """Allow the user to create events from a list"""

    if request.method == "POST":
        eventName = request.form.get("eventName")
        eventDate = request.form.get("eventDate")
        eventPlace = request.form.get("eventPlace")
        eventType = request.form.get("som")
        eventtime = request.form.get("eventtime")
        description = request.form.get("description")
       # print(eventDate)

        # check_time(eventtime)

        if not eventName:
            return apology("please enter the event name")

        if not eventDate:
            return apology("please enter the event date")

        if not eventPlace and not eventPlace.find("vienna"):
            return apology("please enter the event place")
        options = ["Football","Basketball","Runnings", "WinterSports","Climbing","Biking","Soccer"]
        if not eventType in options:
            return apology("please enter the event type")

        if not eventtime:
            return apology("please enter the event date")

        if not description:
            return apology("please enter the event descrtipshen")
        if not check_time(eventDate):
            return apology("invalid time")

        new_event = sql_man.create_new_event(session["id"], eventDate, eventPlace, eventType, eventName,eventtime, description)

        created_event = sql_man.get_created_event(eventName)



        event_id = created_event[0]["index_id"]

        sql_man.join_event(session["id"], event_id)

        ### retrun my page ###

        return redirect('/event/'+ str(event_id))
        #return render_template("event.html", event=created_event)
    else:
        return render_template("create.html")


@app.route("/eventspage", methods=["GET", "POST"])
@login_required
def eventspage():
    events = sql_man.get_available_events()
    if request.method == "POST":

        # validate the event
        if not events:
            flash("there are no events yet")
            return render_template("start.html")


        # knowing which event the user wants to join
        wanted_event = request.form.get("join")

        # getting details for wanted event
        event_details = request.form.get("veiwDetails")

        if event_details:
            render_template("event.html", event = event_details)

        if sql_man.already_participant(session["id"], wanted_event):
            flash("you're already participating!")
            return render_template("eventspage.html", events = events)

        # adding participant to the event
        sql_man.join_event(session["id"], wanted_event)
        flash("you're in!")
        return render_template("eventspage.html", events = events)
    else:
        now = datetime.datetime.now()
        for event in events:
            if parse(event["date"]) <now :
                sql_man.delete_event(event["id"])

        return render_template("eventspage.html", events = events)

@app.route("/mypage", methods=["GET", "POST"])
@login_required
def get_mypage():
    events = sql_man.get_my_events(session["id"])

    if request.method == "POST":
        left_event = request.form.get("leave")
        sql_man.leave_event(session["id"], left_event)
        participants = sql_man.show_participants(left_event)
        if not participants :
            sql_man.delete_event(left_event)
        events = sql_man.get_my_events(session["id"])
        flash("you left the event")
        return render_template("mypage.html", events=events)
    user = sql_man.get_user_infomation(session["id"])
    image = user[0]["image"]
    return render_template("mypage.html", events=events, image=image)

@app.route("/event/<int:index_id>", methods=["GET", "POST"])
@login_required
def event(index_id):
    event = sql_man.show_details(index_id)
    participants = sql_man.show_participants(index_id)

    return render_template("event.html", event = event, participants=participants)


@app.route("/myaccount", methods=["GET", "POST"])
@login_required
def myaccount():
    users = sql_man.get_user_infomation(session["id"])
    if request.method == "POST":
        name  = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        old_password = request.form.get("oldpassword")
      #  image = request.form("file")
        if password != confirmation:
            return apology("sorry password not match")

        if email:
            sql_man.update_user_email(email,session["id"])
            flash("email changed")
        if name:
            sql_man.update_user_name(name,session["id"])
            flash("name changed")
        hashee = sql_man.get_hash(session["id"])
        if password :
            if len(hashee) != 1 or not check_password_hash(hashee[0]["hash"], request.form.get("oldpassword")):
                sql_man.update_user_password(password,session["id"])
                flash("password changed")


        file = request.files['file']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        #if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect("/myaccount")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image = file.filename
            sql_man.update_user_photo(image,session["id"])
            flash("upload file")


        return redirect("/")
   # done.
    return render_template("myaccount.html",name = users[0]["username"], email = users[0]["email"],image=users[0]["image"] )


@app.route("/search/<string:index_id>", methods=["GET", "POST"])
def search(index_id):
    """Search for places that match query"""


