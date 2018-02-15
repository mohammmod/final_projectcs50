from cs50 import SQL
from flask import  request
from flask_session import Session
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

class User_Data:
    def __init__ (self):
        # Configure CS50 Library to use SQLite database
        self.db = SQL("sqlite:///sport.db")

    def create_user(self, username, hash, email, image):
        return self.db.execute("INSERT INTO users (username, hash, email,image) VALUES(:username,:hash, :email,:image)",
                                    username=username,hash= hash, email=email,image=image)

    def get_user_info(self, username):
        return self.db.execute("SELECT * FROM users WHERE username = :username", username=username)

    def check_user(self, email):
        return self.db.execute("SELECT * FROM users WHERE email = :email", email = email)

    def create_new_event(self, id, eventDate, eventPlace, eventType, eventName,eventtime, description):
        return self.db.execute("INSERT INTO events (id ,date, place, type, eventname, created, joined,time, description) VALUES (:id, :date, :place, :type, :eventname, :true, :false,:time, :description)",
                                        id=id, date = eventDate, place = eventPlace ,type = eventType, eventname = eventName, true=1, false=0,time = eventtime, description=description)

    def get_created_event(self, event_name):
        return self.db.execute("SELECT * FROM events WHERE eventname = :eventName", eventName = event_name)

    def get_available_events(self):
        return self.db.execute("SELECT * FROM events WHERE participant = 1 group by eventname")

    def join_event(self, id, event_id):
        username_in_users = self.db.execute("SELECT username FROM users WHERE id = :id", id = id)
        username = username_in_users[0]["username"]
        return self.db.execute("INSERT INTO user_events (user_id, event_id, user_name) VALUES (:id, :event_id, :username)"
                                                                            , id=id, event_id=event_id, username = username)

    def already_participant(self, id, event):
        participants = self.db.execute("SELECT * FROM user_events")
        for participant in participants:
            existed_participant = participant["user_id"]
            existed_event = participant["event_id"]
            if int(existed_participant) == int(id) and int(existed_event) == int(event):
                return True
        return False

    def get_my_events(self, id):
        event_id = self.db.execute("SELECT * FROM user_events WHERE user_id = :id", id=id)
        events = []
        for event in event_id:
            event_name = event["event_id"]
            compare = self.db.execute("SELECT * FROM events WHERE index_id = :event_name", event_name = event_name)
            for line in compare:
                events.append(line)
        return events

    def leave_event(self, id, event_id):

        return self.db.execute("DELETE FROM user_events WHERE user_id = :id and event_id = :event_id", id = id, event_id = event_id)

    def delete_event(self,event_id):
        return self.db.execute("DELETE FROM events WHERE index_id = :event_id",  event_id = event_id)

    def show_details(self, event_id):
        return self.db.execute("SELECT * FROM events WHERE index_id = :event_id", event_id = event_id)

    def show_participants(self, event_id):
        return self.db.execute("SELECT user_name FROM user_events WHERE event_id = :event", event=event_id)

    def get_hash(self, name ):
        return  self.db.execute("SELECT hash FROM users WHERE username = :name ", name = name )

    def get_user_infomation(self, userid):
        return self.db.execute("SELECT * FROM users WHERE id = :userid", userid=userid)

    def update_user_password(self , password, user_id):
        return self.db.execute("UPDATE users SET hash = :password where id = :user_id",
        password = generate_password_hash(password),user_id = user_id)

    def update_user_email(self, email,session):
        return self.db.execute("UPDATE users SET email = :email where id = :user_id",email= email,user_id = session)

    def update_user_name(self, name ,session):
        return self.db.execute("UPDATE users SET username = :name where id = :user_id",name = name,user_id = session)

    def update_user_photo(self,image,id):
        return self.db.execute("UPDATE users SET image = :image where id = :user_id",image = image,user_id = id)

    def get_the_places(self, city):
        return self.db.execute("SELECT * from places where (postal_code like :postcode) or (place_name  like :name) or (admin_name1 like :state)"
        ,postcode = city + '%',name = city +'%' , state = city + '%')


