from flask import Blueprint, redirect, render_template, url_for, session

from ..db import delete_user

# create main frontend blueprint
main = Blueprint(
    "main", __name__, 
    template_folder="templates", 
    static_folder="static"
)

@main.route("/", methods=['GET'])
def index():
    if session['username']:
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for("main.login"))

@main.route("/dashboard", methods=['GET'])
def dashboard():
    if session['username']:
        return render_template(
            'dashboard.html',
            user=session['username']
        )
    else:
        return redirect(url_for("main.index"))

@main.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

@main.route("/logout", methods=['GET'])
def logout():
    delete_user(session['username'])
    session.clear()
    return redirect(url_for('main.login'))

