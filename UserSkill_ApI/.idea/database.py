"""
Creating an instance of SQLAlchemy that will perform the db operations in our CRUD methods
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
