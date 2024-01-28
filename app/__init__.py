from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from dotenv import load_dotenv

# load the environment variables
load_dotenv()

# get the secret key
SECRET_KEY = os.environ.get('APP_SECRET_KEY')

# inititate the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# specify the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


# initiate the database
db = SQLAlchemy()

# initialize the application
db.init_app(app)

# specify the migration
migrate = Migrate(app, db)


# import the models and routes
from . import routes, models