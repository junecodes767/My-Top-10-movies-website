from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float,Date,URL

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base) # creating a db instance

class Movie(db.Model):
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    title:Mapped[str] = mapped_column(String,unique=True)
    year:Mapped[int] = mapped_column(Integer,nullable=False)
    description: Mapped[str] = mapped_column(String,nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=True)
    review: Mapped[str] = mapped_column(String, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    image_url: Mapped[str] = mapped_column(String,nullable=False)
