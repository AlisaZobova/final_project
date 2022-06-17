"""Module with director orm model"""

from .db_init import db


class Director(db.Model):
    """Class to store directors and information about them"""
    __tablename__ = 'director'
    director_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(50), nullable=False)
    surname = db.Column(db.VARCHAR(50), nullable=False)
