"""Configuration module"""

import os


class Config:
    """Configuration class"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
