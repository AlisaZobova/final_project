"""Configuration module"""

import os


class Config:
    """Configuration class"""
    SQLALCHEMY_DATABASE_URI = \
        "postgresql://postgres:postgres_password@test-database:5432/film_library_test"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
