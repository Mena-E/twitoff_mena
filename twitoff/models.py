"""SQLAlchemy User and Tweet models for out database"""
from flask_sqlalchemy import SQLAlchemy

# creates a DB Object from SQLAlchemy class
DB = SQLAlchemy()


# Making a User table using SQLAlchemy
class User(DB.Model):
    """Creates a User Table with SQlAlchemy"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # name column
    name = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):
    """Keeps track of Tweets for each user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    # allows for text and links
    text = DB.Column(DB.Unicode(300))  
    # usier_id column corresponding to user
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False) 
    # Creates user link between tweets
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)



def insert_example_users():
    """Will insert two hypothetical users we've made"""
    mena = User(id=1, name='Mena')
    elon = User(id=2, name='Elon Musk')
    DB.session.add(mena)
    DB.session.add(elon)
    DB.session.commit()


CREATE_USER_TABLE_SQL = """
  CREATE TABLE IF NOT EXIST user (
    id INT PRIMARY,
    name STRING NOT NULL
  );
"""