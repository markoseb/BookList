# [BookListApi](https://github.com/markoseb/BeeBloge)

###This is built with Flask, Flask-RESTful, WTForms, Flask-SQLAlchemy.
###I also used [Google Books Apis](https://developers.google.com/books/docs/v1/using#WorkingVolumes)
Units, integration and system tests with unittest.TestCase

## Download and Installation

To begin using this template:
*	Download on [GitHub](https://github.com/markoseb/BookList)
*	create env with all Packages in [requirements.txt](https://github.com/markoseb/BookList/blob/master/requirements.txt)


## Usage

### Basic Usage

After downloading run:
*	set FLASK_APP=app.py
*	flask db init
*	flask db migrate -m "Create first tabels"
*	flask db upgrade
*	python app.

## About

Using current api version you can: 
* add your own book to db 
* search/edit books in db 
* search books via Google Api and add to local db
* use rest Api to add and search books
