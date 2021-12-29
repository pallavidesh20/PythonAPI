"""
app.py
------
is where our Flask server starts. We create an instance of Flask, set the database path,
initialize db, create an instance of the Api class from flask_restful that will help us create
helper classes for each resource which is to be mapped to an endpoint
"""

from flask import Flask
from flask_restful import Api
from userskills_resource import UserSkillsResource
from database import db
from settings import DATABASE_URL_DEV


def create_app(db_path):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api = Api(app)
    api.add_resource(UserSkillsResource, '/UserSkills','/UserSkills/<id>')
    return app


if __name__ == '__main__':
    app = create_app(DATABASE_URL_DEV)
    app.run(debug=True)
