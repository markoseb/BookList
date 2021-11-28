from book_list import db


class Book(db.Model):
    # Create a table in the db
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    author = db.Column(db.String(140), nullable=False)
    pub_date = db.Column(db.DateTime)
    isbn = db.Column(db.CHAR(17), unique=True, nullable=False)
    pages_number = db.Column(db.Integer())
    link = db.Column(db.NVARCHAR())
    lan = db.Column(db.CHAR(5), nullable=False)

    def __init__(self, title, author, pub_date, isbn, pages, link, language):
        self.title = title
        self.author = author
        self.pub_date = pub_date
        self.isbn = isbn
        self.pages_number = pages
        self.link = link
        self.lan = language

    def __repr__(self):
        return f"Book Id: {self.id} --- Title: {self.title} --- Author: {self.author}"
