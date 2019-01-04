import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///GIMME.db")


@app.route("/")
def index():
    """homepage"""
    return render_template("index.html")


@app.route("/requestpassword",  methods=["GET", "POST"])
def requestpassword():
    """change your password"""
    if request.method == "GET":
        return render_template("requestpassword.html")

    # get email from the form
    email = request.form.get("email")

    # if they do not enter email address, return apology
    if not request.form.get("email"):
        return apology("must provide an email address", 403)

    # if that email is not associated with an account, return apology
    exists = db.execute("SELECT email FROM users WHERE email = :email", email=email)
    if not exists:
        return apology("There is no GIMME account associated with that email address", 403)

    # these are the headers for your message
    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr((str(Header('\U0001F49D GIMME')), 'hawjacollege@gmail.com'))
    msg['To'] = email
    msg['Subject'] = "Get back into your account!"

    # this is the email message that will be sent to the friend
    html = '''\
    <html>
    <head></head>
    <body>
    <p>
    Hello, you've requested a new password! <br>
    click <a href="http://ide50-jamiehawkins.cs50.io:8080/password"> here</a> to change your old one. <br>
    If you didn't request to change your password, then do nothing.  <br>
    </p>
    </body>
    </html>
    '''
    # attach the message to the headers
    msg.attach(MIMEText(html, 'html'))

    # this is the code from lecture that allows you to send an email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("hawjacollege@gmail.com", "Eaglestreet1")
    server.sendmail("hawjacollege@gmail.com", email, msg.as_string())
    server.quit()
    # on send, return to user to the homepage
    return redirect("/")


@app.route("/survey")
def survey():
    """Take a survey"""
    return render_template("survey.html")


@app.route("/surveysend", methods=["GET", "POST"])
def surveysend():
    """send a survey"""
    if request.method == "GET":
        return render_template("surveysend.html")

    # get email, first name name, and message from the form
    email = request.form.get("email")
    first = request.form.get("first")
    extra = request.form.get("extra")

    # if they do not enter a friends email address, return apology
    if not request.form.get("email"):
        return apology("must provide an email address", 403)

    # these are the headers for your message
    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr((str(Header('\U0001F49D GIMME')), 'hawjacollege@gmail.com'))
    msg['To'] = email
    msg['Subject'] = "Someone wants to send you a gift!"

    # this is the email message that will be sent to the friend
    html = '''\
    <html>
    <head></head>
    <body>
    <p>
    Hello ''' + first + ''', your friend is on GIMME! <br>
    They want to send you the perfect gift for a special occasion, <br>
    and they need your help. They're requesting you fill out a <br>
    survey, so you folks here at GIMME can pick out something you're <br>
    sure to love. <br>
    <br>
    <i>''' + extra + '''</i> <br>
    <br>
    Please click <a href="http://ide50-jamiehawkins.cs50.io:8080/surveydofriend" >here</a> to fill it out!
    </p>
    </body>
    </html>
    '''
    # attach the message to the headers
    msg.attach(MIMEText(html, 'html'))

    # this is the code from lecture that allows you to send an email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("hawjacollege@gmail.com", "Eaglestreet1")
    server.sendmail("hawjacollege@gmail.com", email, msg.as_string())
    server.quit()
    # on send, return to user to the homepage
    return redirect("/")


@app.route("/surveydoyou", methods=["GET", "POST"])
def surveydoyou():
    """do a survey"""
    if request.method == "GET":
        return render_template("surveydoyou.html")

    first = request.form.get("first")
    last = request.form.get("last")
    occasion = request.form.get("occasion")
    lifestyle = request.form.get("lifestyle")
    personality = request.form.get("personality")
    age = request.form.get("age")
    rationality = request.form.get("rationality")
    size = request.form.get("size")
    soda = request.form.get("soda")
    terrain = request.form.get("terrain")

    # if they don't fill out all fields... welp.
    if not first or not last or not occasion or not lifestyle or not personality or not age or not rationality or not size or not soda or not terrain:
        return render_template("apology.html", message="Please fill out the entire survey to retrive results.")

    # add survey answers into the survey table
    save_responses = db.execute("INSERT INTO surveys (first, last, occasion, lifestyle, personality, age, rationality, size, soda, terrain) VALUES (:first, :last, :occasion, :lifestyle, :personality, :age, :rationality, :size, :soda, :terrain)",
                                first=first, last=last, occasion=occasion, lifestyle=lifestyle, personality=personality, age=age, rationality=rationality, size=size, soda=soda, terrain=terrain)

    # select the individuals survey response to display on next page
    survey_response = db.execute(
        "SELECT * FROM surveys WHERE first= :first AND last= :last AND occasion= :occasion", first=first, last=last, occasion=occasion)

    # pull only the gifts where the tags include words specified in the survey
    gifts = db.execute("SELECT gift_id, name, image, price, external_link, tags FROM gifts WHERE tags LIKE :occasion AND (tags LIKE :lifestyle OR tags LIKE :personality OR tags LIKE :age OR tags LIKE :rationality OR tags LIKE :size OR tags LIKE :soda OR tags LIKE :terrain)",
                       occasion='%'+occasion+'%', lifestyle='%'+lifestyle+'%', personality='%'+personality+'%', age='%'+age+'%', rationality='%'+rationality+'%', size='%'+size+'%', soda='%'+soda+'%', terrain='%'+terrain+'%')

    # make a list of items from the column name
    name = [gift["name"] for gift in gifts]

    # make a list of items from the column image
    image = [gift["image"] for gift in gifts]

    # make a list of items from the column price
    price = [gift["price"] for gift in gifts]

    # make a list of items from the column external_link
    external_link = [gift["external_link"] for gift in gifts]

    # build entries for html page with individual gift data
    entries = []

    # iterate over the length of the list, name
    for gift in range(len(name)):
        entry = [{"name": gifts[gift]["name"], "image": gifts[gift]["image"], "price": gifts[gift]
                  ["price"], "external_link": gifts[gift]["external_link"]}]
        entries = entries + entry

     # build a structure called gimme so all of this data can be placed in the HTML table
    gimme = {"name": name, "image": image, "price": price, "external_link": external_link, "entries": entries}

    # redirect to GIMME page, which contains filtered gifts
    return render_template("GIMME.html", gimme=gimme, first=first, last=last)


@app.route("/surveydofriend", methods=["GET", "POST"])
def surveydofriend():
    """friend does a survey"""
    if request.method == "GET":
        return render_template("surveydofriend.html")

    first = request.form.get("first")
    last = request.form.get("last")
    occasion = request.form.get("occasion")
    lifestyle = request.form.get("lifestyle")
    personality = request.form.get("personality")
    age = request.form.get("age")
    rationality = request.form.get("rationality")
    size = request.form.get("size")
    soda = request.form.get("soda")
    terrain = request.form.get("terrain")

    # if they don't fill out all fields... welp.
    if not first or not last or not occasion or not lifestyle or not personality or not age or not rationality or not size or not soda or not terrain:
        return render_template("apology.html", message="Please fill out the entire survey to retrive results.")

    # add survey answers into the survey table
    save_responses = db.execute("INSERT INTO surveys (first, last, occasion, lifestyle, personality, age, rationality, size, soda, terrain) VALUES (:first, :last, :occasion, :lifestyle, :personality, :age, :rationality, :size, :soda, :terrain)",
                                first=first, last=last, occasion=occasion, lifestyle=lifestyle, personality=personality, age=age, rationality=rationality, size=size, soda=soda, terrain=terrain)

    # redirect user to home
    return render_template("thanks.html")


@app.route("/GIMME",  methods=["GET", "POST"])
def GIMME():
    """select your gifts"""
    if request.method == "GET":
        return render_template("GIMME.html")
    return redirect("/")


@app.route("/about")
def about():
    """Our story"""
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact Gimme"""
    if request.method == "GET":
        return render_template("contact.html")

    # collect informaion from the message
    occasion = request.form.get("occasion")
    email = request.form.get("email")
    message = request.form.get("message")

    if not occasion or not message:
        return apology("please fill out all required fields", 403)

    # save the message... eventually learn how to email the message to yourself
    save_message = db.execute("INSERT INTO messages (occasion, email, message) VALUES (:occasion, :email, :message)",
                              occasion=occasion, email=email, message=message)

    # on send, return to user to the homepage
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    """Look for friends on GIMME"""
    if request.method == "POST":

        # collect the search term
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        # check the survey database to see if this user has filled out a survey
        pull_surveys = db.execute("SELECT * FROM surveys WHERE first = :first AND last = :last", first=first_name, last=last_name)

        # make a list first names
        first = [survey["first"] for survey in pull_surveys]

        # make a list last names
        last = [survey["last"] for survey in pull_surveys]

        # make a list of occasions
        occasion = [survey["occasion"] for survey in pull_surveys]

        # build entries for html page where you can click to shop for the user
        user_surveys = []

        # iterate over the length of the list, name
        for survey in range(len(pull_surveys)):
            user_survey = [{"first": pull_surveys[survey]["first"], "last": pull_surveys[survey]
                            ["last"], "occasion": pull_surveys[survey]["occasion"]}]
            user_surveys = user_surveys + user_survey

        # build a structure called gimme so all of this data can be placed in the HTML table
        search = {"first": first, "last": last, "occasion": occasion, "user_surveys": user_surveys}

        # Show user their search results
        return render_template("searched.html", first_name=first_name, last_name=last_name, search=search)

    else:
        return render_template("search.html")


@app.route("/searched",  methods=["GET", "POST"])
def searched():
    """see search results"""
    # collect the search term
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        return render_template("GIMMEsearch.html")
    else:
        return render_template("searched.html")


@app.route("/GIMMEsearch", methods=["GET", "POST"])
def GIMMEsearch():
    """access survey results through a search"""
    if request.method == "POST":
        first = request.form.get("first")
        last = request.form.get("last")
        occasion = request.form.get("occasion")
        pull_surveys = db.execute(
            "SELECT * FROM surveys WHERE first = :first AND last = :last AND occasion = :occasion", first=first, last=last, occasion=occasion)

        lifestyle = pull_surveys[0]["lifestyle"]
        personality = pull_surveys[0]["personality"]
        age = pull_surveys[0]["age"]
        rationality = pull_surveys[0]["rationality"]
        size = pull_surveys[0]["size"]
        soda = pull_surveys[0]["soda"]
        terrain = pull_surveys[0]["terrain"]

        # pull only the gifts where the tags include words specified in the survey
        gifts = db.execute("SELECT gift_id, name, image, price, external_link, tags FROM gifts WHERE tags LIKE :occasion AND (tags LIKE :lifestyle OR tags LIKE :personality OR tags LIKE :age OR tags LIKE :rationality OR tags LIKE :size OR tags LIKE :soda OR tags LIKE :terrain)",
                           occasion='%'+occasion+'%', lifestyle='%'+lifestyle+'%', personality='%'+personality+'%', age='%'+age+'%', rationality='%'+rationality+'%', size='%'+size+'%', soda='%'+soda+'%', terrain='%'+terrain+'%')

        # make a list of items from the column name
        name = [gift["name"] for gift in gifts]

        # make a list of items from the column image
        image = [gift["image"] for gift in gifts]

        # make a list of items from the column price
        price = [gift["price"] for gift in gifts]

        # make a list of items from the column external_link
        external_link = [gift["external_link"] for gift in gifts]

        # build entries for html page with individual gift data
        entries = []

        # iterate over the length of the list, name
        for gift in range(len(name)):
            entry = [{"name": gifts[gift]["name"], "image": gifts[gift]["image"], "price": gifts[gift]
                      ["price"], "external_link": gifts[gift]["external_link"]}]
            entries = entries + entry

        # build a structure called gimme so all of this data can be placed in the HTML table
        gimme = {"name": name, "image": image, "price": price, "external_link": external_link, "entries": entries}
        return render_template("GIMMEsearch.html", gimme=gimme, first=first, last=last)
    else:
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via GET (clicking register link from homepage)
    if request.method == "GET":

        """Register user"""
        return render_template("register.html")

    # access the info the user submitted in the html template
    # reference the input name from html
    first = request.form.get("first")
    last = request.form.get("last")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # make sure all fields are filled in
    # if any fields are left blank, return apology
    if not first or not last or not email or not username or not password or not confirmation:
        return apology("Please make sure to fill out all required fields")

    # make sure password and confirmation match... otherwise, apologize again
    if password != confirmation:
        return apology("Password and confirmation do not match")

    # instead of storing the password , store a hash of the password
    hash = generate_password_hash(password)

    # access the SQL database
    db = SQL("postgres://ibknbtfhpwxchz:c23288bf14e52e38013d13ec7dc75e8d904da228d874bf280fde910e0eb8b559@ec2-54-83-197-230.compute-1.amazonaws.com:5432/d5d9o49nj35bui")

    # username and userid should be unique
    # if the username is already in the data base, db.execute should fail
    already_exists = db.execute("SELECT username FROM users WHERE username = :username", username=username)
    if already_exists:
        return apology("That username already exists...")

    # next add the user to the database so they are stored
    add_user = db.execute("INSERT INTO users (username, hash, first, last, email) VALUES (:username, :hash, :first, :last, :email)",
                          username=username, hash=hash, first=first, last=last, email=email)

    # once the user registers successfully, log them in automatically
    if add_user:
        # store their id in session
        session["user_id"] = add_user

    # direct the user to the homepage
    return redirect("/")


@app.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "GET":

        return render_template("password.html")

    # access the info the user submitted in the html template
    # reference the input from html
    username = request.form.get("username")
    new_password = request.form.get("new_password")
    confirmation = request.form.get("confirmation")

    # make sure all fields are filled in
    # if any fields are left blank, return apology
    if not username or not new_password or not confirmation:
        return apology("Please make sure to fill out all required fields")

    # make sure that username exists in the database
    already_exists = db.execute("SELECT username FROM users WHERE username = :username", username=username)
    if not already_exists:
        return apology("That username does not exist…")

    # make sure password and confirmation match... otherwise, apologize again
    if new_password != confirmation:
        return apology("Password and confirmation do not match")

    # instead of storing the new password , store a hash of the password
    hash = generate_password_hash(new_password)

    # next replace the users old password with the new one in the database
    change_password = db.execute("UPDATE users SET hash = :hash WHERE username = :username", hash=hash, username=username)

    # once the user successfully changes their password, redirect them to the login page to log in as normal
    return redirect("/login")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
