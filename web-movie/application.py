import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import base64
#from flask_mail import Mail, Message
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import inr, login_required, convertToBinaryData


#Configure application
app = Flask(__name__)

#Ensure templates are reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configuring session to use filesystem (no cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///project.db")


flag = 0

#have to Comfigure the database connection
@app.route("/")
def route():
    if session.get("user-id") is None:
        return redirect("/logo")

    else:
        return redirect("/home")



@app.route("/logo")
def logo():
    return render_template("logo.html")



@app.route("/admin")
@login_required
def admin():
    if session['user'] is not None:
        row = db.execute("SELECT username, email from users where id=:id",
                          id = session['user-id'])

        return render_template("admin.html", admin = row[0]["username"], email = row[0]["email"])



@app.route("/ns")
@login_required
def nowshow():

    row = db.execute("SELECT poster FROM movies")

    posters =[]

    for movie in row:
        posters.append(base64.b64encode(movie["poster"]).decode("utf-8"))

    return render_template("nowshow.html", posters=posters)


@app.route("/showm")
@login_required
def showmovies():
    row = db.execute("Select name,Language,length,genre,Trailer,\"Cast\",Director,Rating,About from movies")
    text = ""
    for movie in row:
        text +="<movie><name>"+movie["name"]+"</name><lang>"+movie['Language']+"</lang><len>"+str(movie['length'])+"</len><genre>"+movie['genre']+"</genre><url>"+movie['Trailer']+"</url><cast>"+movie['Cast']+"</cast><dir>"+movie['Director']+"</dir><rating>"+movie['Rating']+"</rating><about>"+movie['About']+"</about></movie>"
    return text


@app.route("/regadmin", methods=['GET', 'POST'])
@login_required
def reg_admin():
    row = db.execute("SELECT username, email from users where id=:id",
                          id = session['user-id'])

    if request.method == "GET":
        #flash(u"admin reg")
        return render_template("regadmin.html",  admin = row[0]["username"], email = row[0]["email"], regadmin = "active")

    else:
        name = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        contact = request.form.get("contact")

        prim_key = db.execute("INSERT INTO users (username, password, email, contact, category) VALUES(:username, :password, :email, :contact, :category)",
                                username = name,
                                password = generate_password_hash(password),
                                email = email,
                                contact = contact,
                                category = 1)

        if prim_key is not None:
            flash(u"Record is added to database")

        else:
            flash(u"Record is not added to database")

        return render_template("regadmin.html", admin = row[0]["username"], email = row[0]["email"], regadmin= "active")



@app.route("/home")
@login_required
def log():
    if request.method == "GET":

        row = db.execute("SELECT poster, name, Language FROM movies")

        posters =[]
        names = []
        lang=[]

        for movie in row:
            posters.append(base64.b64encode(movie["poster"]).decode("utf-8"))
            names.append(movie["name"])
            lang.append(movie["Language"])

        return render_template("movie.html", moviePosters=zip(posters,names, lang))



@app.route("/db")
@login_required
def dashb():
    row = db.execute("SELECT username, email from users where id=:id",
                          id = session['user-id'])

    flash(u"admin")
    return render_template("dashboard.html", admin = row[0]["username"], email = row[0]["email"], db="active")




@app.route("/login", methods=["GET", "POST"])
def index():
    """User log in """
    session.clear()

    if request.method == "GET":
        return render_template("signin.html")


    else:
        row = db.execute("SELECT * FROM users WHERE username=:username",
                          username=request.form.get("username"))

        if len(row) != 1 or not check_password_hash(row[0]["password"], request.form.get("password")):
            flag = 1
            return render_template("signin.html", alert= 1)

        else:
            session['user-id'] = row[0]["id"]
            if(row[0]["category"] == 1):
                session['user'] = "admin"
                return redirect("/admin")

            return redirect("/")





@app.route("/register", methods=["GET", "POST"])
def reg():
    """User Register"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        name = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        contact = request.form.get("contact")

        prim_key = db.execute("INSERT INTO users (username, password, email, contact, category) VALUES(:username, :password, :email, :contact, :category)",
                                username = name,
                                password = generate_password_hash(password),
                                email = email,
                                contact = contact,
                                category = 0)
        #Check it out
        session['user-id'] = prim_key

        return redirect("/home")




''' name="Vakeel Saab"
    iden = 5
    poster = "static/movies/vakeelsaab.jpg"
    lang = "Telugu"
    length = 153
    genre = "Action, Drama, Thriller"
    issue = 1
    movie_show = 1
    Trailer = "https://www.youtube.com/embed/P1xKV0Dmetg?autoplay=1&mute=0"
    Cast = "Pawan Kalyan, Nivetha Thomas, Anjali, Ananya Nagalla, Prakash Raj"
    Director = "Sriram Venu"
    About = "When three young women are implicated in a crime, a retired lawyer steps forward to help them clear their names."
    prim_key = db.execute("INSERT INTO movies (id, name, Language,  poster, length, genre, issue, movie_show, Trailer, Cast, Director, Rating, About) VALUES(:id, :name, :language,  :poster, :length, :genre, :issue, :movie_show, :Trailer, :Cast, :Director, :Rating, :About )",
                           id = iden,
                           name = name,
                           language = lang,
                           poster = convertToBinaryData(poster),
                           length = length,
                           genre = genre,
                           issue = issue,
                           movie_show = movie_show,
                           Trailer = Trailer,
                           Cast = Cast,
                           Director = Director,
                           Rating = "U/A",
                           About = About)


    prim_key = db.execute("INSERT INTO users (username, password, email, contact, category) VALUES(:username, :password, :email, :contact, :category)",
                                username = "ReelCin",
                                password = generate_password_hash("Reel@6720"),
                                email = "admin@reelcinemas.com",
                                contact = "99345",
                                category = 1) '''