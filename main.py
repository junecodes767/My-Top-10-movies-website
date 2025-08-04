from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired
import requests
from models import Movie,db
from flask_migrate import Migrate
from sqlalchemy import desc

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collection.db"
db.init_app(app)


migrate = Migrate(app, db)

with app.app_context():
    # db.drop_all()
    db.create_all()

# with app.app_context():

#     second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     image_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
#     db.session.add(second_movie)
#     db.session.commit()
        
# CREATE DB


# CREATE TABLE

class edit_rating_ranking_form(FlaskForm):
    rating = IntegerField('Rating',validators=[DataRequired()])
    review = StringField('Review',validators=[DataRequired()])
    submit = SubmitField('Submit',validators=[DataRequired()])
    
@app.route("/")
def home():
    # movies = Movie.query.all()
    movies = list(db.session.execute(db.select(Movie).order_by(desc(Movie.rating))).scalars())

    return render_template("index.html",movie=movies)

class addMovies(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    submit = SubmitField('Add Movie', validators=[DataRequired()])
    
    
    
@app.route("/select/<name>", methods =["GET","POST"])    
def select(name):

    url = f"https://api.themoviedb.org/3/search/movie?query={name}&include_adult=true&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NjM4NWY2MDhmYzM2ZWIxNWNhMjUwMjk0MmZmZmU0YSIsIm5iZiI6MTc1Mzc5OTkxNy45NTM5OTk4LCJzdWIiOiI2ODg4ZGNlZDIwZTUxZDYxYjcyNDdiZTEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.TgCDVgywVNN2QzLDYjPyM3-AbKCdwqs7-wr1BDlMqIQ"
    }

    response = requests.get(url, headers=headers)
    movies = response.json()["results"]
    return render_template('select.html', movies = movies)

@app.route("/select-movie/<int:id>", methods =["GET","POST"])    
def select_movies(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NjM4NWY2MDhmYzM2ZWIxNWNhMjUwMjk0MmZmZmU0YSIsIm5iZiI6MTc1Mzc5OTkxNy45NTM5OTk4LCJzdWIiOiI2ODg4ZGNlZDIwZTUxZDYxYjcyNDdiZTEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.TgCDVgywVNN2QzLDYjPyM3-AbKCdwqs7-wr1BDlMqIQ"
    }
    TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

    response = requests.get(url, headers=headers)
    description = response.json()["overview"]
    title = response.json()["original_title"]
    image_url = TMDB_IMAGE_BASE_URL + response.json()["poster_path"] 
    year = response.json()["release_date"]
    new_movie = Movie(id = id , title = title, image_url = image_url, year = year, description = description)
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit',id= id ))
    
    
    
@app.route("/add",methods =["POST","GET"])
def add():
    form = addMovies()
    
    if form.validate_on_submit():
        name  = form.title.data
        return redirect(url_for('select', name = name ))
    return render_template("add.html",form = form)

@app.route("/delete/<int:id>")
def delete(id):
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home')) 



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    form = edit_rating_ranking_form()
    if Movie is None:
        return "Movie not found", 404  # Or handle it however you'd like
    if form.validate_on_submit():
        new_review = form.review.data
        new_rating = form.rating.data
        if new_rating <=10:
            movie_to_update = db.session.execute(db.select(Movie).where(Movie.id ==id)).scalar()
            movie_to_update.rating = new_rating
            movie_to_update.review= new_review
            db.session.commit() 
            return redirect(url_for('home'))   
    return render_template('edit.html',form = form)
    



if __name__ == '__main__':
    app.run(debug=True)
