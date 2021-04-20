"""This is what brings the application together"""
from flask import Flask, render_template
from .models import DB, User, insert_example_users


def create_app():
    """
    The main app function for twitoff.
    Brings everything together.
    """
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONs"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        # Drops everything from DB
        DB.drop_all()
        # Creates DB
        DB.create_all()
        insert_example_users()
        return render_template('base.html', title = "Home")

    @app.route('/hola')
    def hola():
        return "Hola, Twitoff"

    @app.route('/salut')
    def salut():
        return "Salut, Twitoff"

    return app
