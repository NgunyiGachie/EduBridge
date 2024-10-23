"""
Database initialization module for Flask application.
This module sets up SQLAlchemy and Flask-Migrate for the application.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize the database with the given Flask app."""
    try:
        db.init_app(app)
        migrate.init_app(app, db)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database: {e}")
