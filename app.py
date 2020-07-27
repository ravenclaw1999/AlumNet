# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo


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
    if request.method == "GET":
        return render_template("login.html")
    else:
        if request.form["action"] == "signin":
            print(request.form)
            username = request.form["username"]
            password = request.form["password"]
            users = mongo.db.users
            login_user = users.find_one({'username' : username})
            if login_user:
                if password == login_user['password']:
                    session['name'] = login_user["name"]
                    return render_template("index.html")
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
                users.insert({'username': username, 'password': password, 'name': name, 'email' : email, 'grad_year': grad_year})
                session['name'] = name
                return render_template("index.html")
            return 'That username already exists! Try logging in.'
# LOG OUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
# PROFILE
# methods tbd


@app.route('/profile')
def profile():
    users = mongo.db.users
    user = users.find_one({'name' : request.form['select']})
    # select is a placeholder until we figure how to use search or reroute from my_profile
    return render_template("profile.html", user = user)


# EDITING PROFILE
@app.route('/my-profile', methods = ["GET","POST"])
def my_profile():
    users = mongo.db.users
    name = session["name"]
    user = users.find_one({'name': name})
    if request.method == "GET":
        return render_template("my_profile.html", user = user)
    else: 
        bio = request.form("bio")
        birthday = request.form("birthday")
        grad_year = request.form("grad_year")
        cohort = request.form("cohort")
        user.insert({"bio": bio, "birthday": birthday, "grad_year": grad_year, "cohort": cohort})
        return render_template("profile.html", user = user)


# PROFILE_LIST
# Jinja loops?
@app.route('/profile-list')
def profile_list():
    users = mongo.db.users
    return render_template("profile_list.html", users = users)


#ARTICLES
# Store articles through mongoDB? Also Jinja loops?
@app.route('/articles')
def articles():
    articles = mongo.db.articles
    return render_template("articles.html")

@app.route('/bio', methods=["GET", "POST"])
def bio():
    return render_template("bio.html")
