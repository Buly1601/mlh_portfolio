import os
from flask import Flask, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

# main page    
@app.route('/')
def index():
    return render_template('main_page.html', title="MLH Fellow", url=os.getenv("URL"))

# external pages    
@app.route("/projects")
def carousel():
    return render_template("projects.html", title="works", url=os.getenv("URL"))

@app.route("/about")
def about_me():
    return render_template("about_me.html", title="about_me", url=os.getenv("URL"))

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact", url=os.getenv("URL"))

@app.route("/contact-successful")
def contact_sucessful():
    return render_template("contact_success.html", title="Contact", url=os.getenv("URL"))

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return f"User {username} created successfully"
        else:
            return error, 418

    # TODO implement the register page
    return "NOT YET IMPLEMENTED\n", 501

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            return "Login Successful", 200
        else:
            return error, 418

    # TODO implement the login page
    return render_template("login.html", title="Login", url=os.getenv("URL"))

# health checker for vital signs    
@app.route("/health")
def healthy():
    return ''
