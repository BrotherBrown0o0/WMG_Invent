import os
from datetime import timedelta

# Get the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session signing, csrf protection, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Ensure SQLite database is stored in the instance folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.sqlite')
    
    # Disable SQLAlchemy modification tracking (improves performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Set session timeout to 60 minutes
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60) 