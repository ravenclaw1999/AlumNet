# ---- YOUR APP STARTS HERE ----
# -- Import section --

from flask import Flask
from flask import render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
import bcrypt


# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'alumnet'

# URI of database
app.config['MONGO_URI'] = "mongodb+srv://admin:Fqt5QCXcayFPRj9Q@cluster0.k1fjy.mongodb.net/alumnet?retryWrites=true&w=majority"
mongo = PyMongo(app)


app.secret_key='5mJDS*$26loJ'


# -- Routes section --
# HOME
# Session id (HTML)?
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
        if request.form["action"] == "signin":
            username = request.form["username"]
            password = request.form["password"]
            users = mongo.db.users
            login_user = users.find_one({'username' : username})
            if bcrypt.hashpw(password.encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['name'] = login_user["name"]
                return "Welcome!  You are logged in as " + login_user["name"] + ".  Go to <a href='/bio'>bio</a>."
            else:
                return 'Invalid username/password combination'
        elif request.form["action"] == "signup":
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
                return "Welcome!  You are logged in as " + session["name"] + ".  Go to <a href='/bio'>bio</a>."
            return 'That username already exists! Try logging in.'



# LOG OUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# PROFILE
# methods tbd
# EDITING PROFILE
# @app.route('/my-profile', methods = ["GET","POST"])
# def my_profile():
#     users = mongo.db.users
#     name = session["name"]
#     user = users.find_one({'name': name})
#     if request.method == "GET":
#         return render_template("my_profile.html", user = user)
#     else: 
#         bio = request.form("bio")
#         birthday = request.form("birthday")
#         grad_year = request.form("grad_year")
#         cohort = request.form("cohort")
#         user.insert({"bio": bio, "birthday": birthday, "grad_year": grad_year, "cohort": cohort})
#         return render_template("profile.html", user = user)
# PROFILE_LIST
# Jinja loops?
@app.route('/alum')
def alum():
    collection = mongo.db.users
    users = collection.find({})
    return render_template("alum.html", users = users)


# ARTICLES
# Store articles through mongoDB? Also Jinja loops?
@app.route('/articles')
def articles():
    articles = mongo.db.articles
    return render_template("articles.html")
    
# BIO
@app.route('/bio', methods=["GET", "POST"])
def bio():
    users = mongo.db.users
    if 'name' in session:
        name = session['name']
        user = users.find_one({'name': name})
        return render_template("bio.html", user = user)
    else:
        return "Please log in."