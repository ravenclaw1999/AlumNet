# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
import bcrypt
import datetime
import os
from dotenv import load_dotenv

# -- Initialization section --
app = Flask(__name__)

#SECRET KEY
load_dotenv()
app.secret_key = os.getenv("KEY")

# name of database
app.config['MONGO_DBNAME'] = 'alumnet'

# URI of database
app.config['MONGO_URI'] = os.getenv("MONGO_URI")

mongo = PyMongo(app)


# -- Routes section --
# HOME
@app.route('/')
@app.route('/index', methods = ["GET", "POST"])
def index():
    return render_template("index.html")

# LOGIN/SIGNUP
@app.route('/login', methods = ["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        print("hi")
        if request.form["action"] == "Login":
            username = request.form["username"]
            password = request.form["password"]
            users = mongo.db.users
            login_user = users.find_one({'username' : username})
            if bcrypt.hashpw(password.encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['name'] = login_user["name"]
                session['username'] = login_user["username"]
                return redirect(url_for('bio'))
            else:
                return 'Invalid username/password combination'
        elif request.form["action"] == "Sign Up":
            users = mongo.db.users
            existing_user = users.find_one({'username' : request.form['new_username']})
            if existing_user is None:
                username = request.form["new_username"]
                password = request.form["new_password"]
                name = request.form["new_name"]
                email = request.form["new_email"]
                grad_year = request.form["grad_year"]
                users.insert({'username': username, 'password': str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8'), 'name': name, 'email' : email, 'grad_year': grad_year})
                session['name'] = name
                session['username'] = username
                return redirect(url_for('updateInfo'))
            return 'That username already exists! Try logging in.'

# BIO
@app.route('/bio', methods=["GET", "POST"])
def bio():
    users = mongo.db.users
    post_collection = mongo.db.posts
    if 'name' in session:
        username = session['username']
        user = users.find_one({'username': username})
        posts = post_collection.find({'author': username})
        return render_template("bio.html", user = user, posts = posts)
    else:
        return "Please log in."

# UPDATE INFO
@app.route('/update-info', methods = ["GET","POST"])
def updateInfo():
    users = mongo.db.users
    username = session["username"]
    if request.method == "GET":
        return render_template("updateInfo.html", username = username)
    else: 
        name = request.form["name"]
        email = request.form["email"]
        if request.form["image_url"] == "":
            image_url = "https://media-exp1.licdn.com/dms/image/C4E0BAQE6lQtEKdA5dw/company-logo_200_200/0?e=2159024400&v=beta&t=UeYB5MUD2arx7SRkE4rd9FU-2dMIJAq83Ne8RonjrwE"
        else:
            image_url = request.form["image_url"]
        bio = request.form["bio"]
        birthday = request.form["birthday"]
        college = request.form["college"]
        major = request.form["major"]
        intended_career = request.form["intended_career"]
        cohort = request.form["cohort"]
        update = users.update_many(
            {"username": username}, 
            {
                "$set": {"name": name, "email": email, "bio": bio, "birthday": birthday, "cohort": cohort, "college": college, "major": major, "intended_career": intended_career, "image_url": image_url}
            })
        return redirect(url_for('bio'))

# PROFILE_LIST
@app.route('/alum')
def alum():
    collection = mongo.db.users
    users = collection.find({})
    return render_template("alum.html", users = users)

# ARTICLES
@app.route('/articles')
def articles():
    articles = mongo.db.articles
    return render_template("articles.html")

# PROFILE
@app.route('/profile/<username>', methods=["GET", "POST"])
def profile(username):
    users = mongo.db.users
    post_collection = mongo.db.posts
    user = users.find_one({'username': username})
    posts = post_collection.find({'author': username})
    return render_template("profile.html", user = user, posts = posts)

# MAKE POST
# Code borrowed from Daniel Choi and Alice Yeh
@app.route('/make-post', methods=["GET", "POST"])
def makepost():
    if 'name' in session:
        if request.method == "POST":
            post_collection = mongo.db.posts
            username = session['username']
            title = request.form["post-title"]
            message = request.form["post-message"]
            date = datetime.datetime.now()
            post = {
                "title" : title,
                "message" : message,
                "date" : date,
                "author" : username
            }
            post_collection.insert(post)
            return redirect(url_for('bio'))
        else:
            return render_template("post.html")
    else:
        return "Please log in."
