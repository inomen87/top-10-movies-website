from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, URL
import requests
from sqlalchemy.exc import OperationalError



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)



class Movies(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   year  = db.Column(db.Integer, nullable=False)
   title  = db.Column(db.String(250), nullable=False)
   description  = db.Column(db.String(500), nullable=False)
   review  = db.Column(db.String(2000), nullable=False)
   img_url  = db.Column(db.String(500), nullable=False)
   rating = db.Column(db.Float(), nullable=False)
   ranking = db.Column(db.Integer, nullable=False)

   def __init__(self, title, year, description, review, img_url, rating, ranking):
      self.title = title
      self.year = year
      self.description = description
      self.review = review
      self.img_url = img_url
      self.rating = rating
      self.ranking = ranking




def open_db():
    with app.app_context():
        try:
            all_movies = Movies.query.all()
        except sqlalchemy.exc.OperationalError:
            db.create_all()
        finally:
            all_movies = list(db.session.execute(db.select(Movies)).scalars())
            all_movies = {movie.id: {"title": movie.title, "year": movie.year, "review": movie.review,  "img_url": movie.img_url, "rating": movie.rating, "ranking": movie.ranking} for movie in all_movies}

    print(all_movies)
    return all_movies

open_db()





@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
