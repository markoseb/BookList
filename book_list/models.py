import datetime

from book_list import db
from dateutil import parser as dataparser
from flask import flash


class Book(db.Model):
    # Create a table in the db
    __tablename__ = 'books'

    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(140), nullable=False)
    author          = db.Column(db.String(140), nullable=False)
    pub_date        = db.Column(db.DateTime)
    isbn            = db.Column(db.CHAR(17), unique=True, nullable=False)
    pages_number    = db.Column(db.Integer())
    link            = db.Column(db.NVARCHAR())
    lan             = db.Column(db.CHAR(5), nullable=False)

    def __init__(self, title, author, pub_date, isbn, pages_number, link, lan):
        self.title          = title
        self.author         = author
        self.pub_date       = dataparser.parse(pub_date)
        self.isbn           = isbn
        self.pages_number   = pages_number
        self.link           = link
        self.lan            = lan



    def __repr__(self):
        return f"Book Id: {self.id} --- Title: {self.title} --- Author: {self.author}"

    def json(self):
        return {
            'title'         : self.title,
            'author'        : self.author,
            'pub_date'      : self.pub_date.strftime("%Y-%m-%d"),
            'isbn'          : self.isbn,
            'pages_number'  : self.pages_number,
            'link'          : self.link,
            'lan'           : self.lan,
        }
    @classmethod
    def find_by_isbn(cls,isbn):
        return cls.query.filter_by(isbn=isbn).first()

    def save_to_db(self):
        if self.query.filter_by(isbn=self.isbn).first() or self.pub_date > datetime.datetime.now():
            flash(f"Książka o podanym ISBN = {self.isbn} już istnieje, lub wpisana data publikacji jest z przyszłości")
            return False
        else:
            db.session.add(self)
            db.session.commit()
            return True


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
