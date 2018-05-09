# design ---------- mohammad sawas, yazan kassoua ,thaer ohda , Nourallah Takie Alddin



Our final project “sports event “  is a website that meant to be for everyone who likes sport and wants
to meet up with new people as well.My goal was for this website to be as functional, intuitive,
and aesthetically pleasing as possible,plus I wanted to help people who liked sport like my brother.

The user begins with either logging in or registering for an account. In both cases,
flask and python via the SQLQuery are used dynamically to activate user account and at the same time,
the user details are going to be super secure because we are going to create a hash of there passwords.
If the user is registering for the first time via some code of python s/he will get a notification E-mail welcoming him/her
at our platform,we save the image in the static file and save the URL in the SQL database.

After logging in, the user will be able to see an HTML page with a nice welcoming note using flask render_template function.
and there will be two buttons that are connecting with two URLs the first one with "/create" which will be connected with
“create an event “ and the second one with "/events page" the biggest challenge for this page was dealing with buttons,
through GET method.However, there will result also two cases:

The first case if the user clicks on “create an event” the function of the index will redirect the user to "/create" page
where the user could insert a new event, and there will be some labels that are connecting with python code,
and for that Many functions were implemented to make sure the user could be flexible in the format of their event details,
like the user could not enter a non-date or chronologically-wrong date into the database, the user could see a small map and
some suggestion of places that he could make his event in, for the map configuration we had to use jQuery and the rest were
pythons -SQL -HTML -CSS and after the user has created the event he will be redirected to "/event/{eventnumber}
where we show the user the details of their event by selecting them from the database and send them to HTML page
where they will be managed by templating languge which is called JINJA.

The second case if the user clicks on “join an event”  the user will be redirected to the URL"/eventpage"
using redirect function - python. where we just select all the event from the database and send them to the HTML page and,
this will be managed using jinja.at. At the same time there will be a button called join which is connected with python code and,
the user will be added to the database as "going" to this event. The name of the event will be also as a link that leads the user
to the event details. and for sure we get this link from "HTML"  and a number of the event from "databases".

At the navbar, the user has also my page under the URL"/my page" where s/he sees a list of the event that s/he is participating in.
And these details once again are coming for sure from the database and they are managed by JINJA.
there will be also one button called “leave” and guess what happened when the user clicks it:).
This button will be connecting with the python code which connects to the database and ,
it will immediately update in SQL as left the event.

There is also account settings where you will see labels and you could change the user name,
password, and even your image and for sure all of that is going to be updated in the database and also in the static files.

And now for the most incredible page under the URL"/about" where the users will be able to see the developers
that have worked on this project, for that we only used python and flask library to show this static page.