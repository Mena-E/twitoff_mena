"""This is what brings the application together"""
from os import getenv 
from flask import Flask, render_template
from .models import DB, User
from .twitter import add_or_update_user


def create_app():
    """
    The main app function for twitoff.
    Brings everything together.
    """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initializing database
    DB.init_app(app)

    # decorator checks for specifci endpoint visits
    @app.route('/') # http://127.0.0.1:500/
    def root():
        # Drops everything from DB
        DB.drop_all()
        # Creates DB
        DB.create_all
        return render_template('base.html', title = "Home")


    @app.route('/reset')
    def reset():
        # Drops everything from DB, then creates a new DB
        DB.drop_all()
        DB.create_all()
        return "Database reset!"


    @app.route('/addusers')
    def add_users():
        # adding users
        add_or_update_user("mena")

    return app
