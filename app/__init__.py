import os
from flask import request, Flask, render_template, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
import db

# Flask uses load_dotenv by default
app = Flask(__name__)	

# add the datbase
app.config["DATABASE"] = os.path.join(os.getcwd(), "flask.sqlite")
db.init_app(app)

# main page    
@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

# external pages    
@app.route("/projects")
def carousel():
    return render_template("carousel.html", title="works", url=os.getenv("URL"))

@app.route("/about")
def about_me():
    return render_template("about_me.html", title="about_me", url=os.getenv("URL"))

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact", url=os.getenv("URL"))

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif db.execute(
            "SELECT id FROM user WHERE username = ?", (username)
            ).fetchone() != None:
            error = f"user {username} already exists"
        
        if error == None:
            db.execute(
                "INSERT INTO user (username,password) VALUES (?,?)",
                (username, generate_password_hash(password))
            )
            db.commit()
            return f"user {username} created successfully"
        else:
            return error, 418

    # TODO implement the register page
    return "NOT YET IMPLEMENTED\n", 501

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username)
        ).fetchone()

        if not user:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
                error = "Incorrect password."
        
        if not error:
            return "Login successful", 200
        else:
            return error, 418

    # TODO implement the login page
    return render_template("login.html", title="Login", url=os.getenv("URL"))

# health checker for vital signs    
@app.route("/health")
def healthy():
    return ''