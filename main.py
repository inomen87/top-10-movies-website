from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, FloatField, TextAreaField
from wtforms.validators import DataRequired, URL
import requests
from sqlalchemy.exc import OperationalError



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)







class EditForm(FlaskForm):
    rating = FloatField('Your Rating', validators=[DataRequired()], render_kw={'style': 'width: 40ch'})
    review = TextAreaField('Your Review', render_kw={'style': 'width: 40ch'})

    submit = SubmitField('Done')







class Movies(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   year  = db.Column(db.Integer, nullable=False)
   title  = db.Column(db.String(250), nullable=False)
   description  = db.Column(db.String(500), nullable=False)
   review  = db.Column(db.String(2000))
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
            all_movies = {movie.id: {"title": movie.title, "year": movie.year, "review": movie.review,  "img_url": movie.img_url, "rating": movie.rating, "ranking": movie.ranking, "description": movie.description} for movie in all_movies}

    print(all_movies)
    return all_movies






@app.route("/")
def home():
    return render_template("index.html", movielist=open_db())




@app.route("/edit/<movie_id>", methods=('GET', 'POST'))
def edit(movie_id):
    form = EditForm()
    print(type(request.form))
    if form.validate_on_submit():
        with app.app_context():
            movie_to_update = db.session.execute(db.select(Movies).where(Movies.id == movie_id)).scalar()
            movie_to_update.rating = request.form["rating"]
            movie_to_update.review = request.form["review"]
            db.session.commit()

        return redirect(url_for('home'))

    return render_template("edit.html", form=form, movie_id=int(movie_id), movielist=open_db())




@app.route("/delete/<movie_id>", methods=('GET', 'POST'))
def delete(movie_id):
    form = EditForm()
    print(type(request.form))
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movies).where(Movies.id == movie_id)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
