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
                return "Welcome!  You are logged in as " + login_user["name"] + ". Go to <a href='/bio'>bio</a>."
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
                return "Welcome!  You are logged in as " + session["name"] + ". Go to <a href='/update-info'>Update Info</a>."
            return 'That username already exists! Try logging in.'
# BIO
@app.route('/bio', methods=["GET", "POST"])
def bio():
    users = mongo.db.users
    if 'name' in session:
        username = session['username']
        user = users.find_one({'username': username})
        return render_template("bio.html", user = user)
    else:
        return "Please log in."
# Update Info
@app.route('/update-info', methods = ["GET","POST"])
def updateInfo():
    users = mongo.db.users
    username = session["username"]
    if request.method == "GET":
        return render_template("updateInfo.html", username = username)
    else: 
        name = request.form["name"]
        email = request.form["email"]
        bio = request.form["bio"]
        birthday = request.form["birthday"]
        cohort = request.form["cohort"]
        update = users.update_many(
            {"username": username}, 
            {
                "$set": {"name": name, "email": email, "bio": bio, "birthday": birthday, "cohort": cohort}
            })
        return "Your info has been updated, " + session["name"] + ". Go to <a href='/bio'>bio</a> to see new updates."
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
# MAKE POST
@app.route('/makepost', methods=["GET", "POST"])
def makepost():
    print("Hi")
    if request.method == "POST":
        post_collection = mongo.db.posts
        logged_in_username = session['username']
        # user = user_collection.find_one({"username" : logged_in_username})
        title = request.form["post-title"]
        message = request.form["post-message"]
        # date = datetime.now()
        post = {
            "title" : title,
            "message" : message,
            # "date" : date,
            "author" : logged_in_username
        }
        post_collection.insert(post)
        return "It worked"
    else:
        return render_template("post.html")