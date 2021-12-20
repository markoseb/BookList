import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)

db = SQLAlchemy(app)
Bootstrap(app)

app.config['SECRET_KEY'] = config["SECRET_KEY"]["SECRET_KEY"]

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_HASH'] = config["SECURITY_PASSWORD"]["HASH"]
app.config['SECURITY_PASSWORD_SALT'] = config["SECURITY_PASSWORD"]["SALT"]



Migrate(app, db)

from book_list.core.views import core
from book_list.books.views import books
from book_list.book_api.views import book_api

app.register_blueprint(core)
app.register_blueprint(books)
app.register_blueprint(book_api)


from flask_restful import Api
from .rest_api.views import BookFilter, BookDb
api = Api(app)

api.add_resource(BookFilter, "/bookfilter/<string:title>/<string:author>/<string:lan>/<string:data_str>/<string:data_end>")
api.add_resource(BookDb, "/bookdb")
