from flask_restful import Resource, reqparse

from book_list.core.views import search_book
from book_list.models import Book


class BookDb(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("title",
                        type=str,
                        help="Write title")
    parser.add_argument("author",
                        type=str,
                        help="Write author name")
    parser.add_argument("pub_date",
                        type=str,
                        help="Write start date like : 2020-12-18")
    parser.add_argument("isbn",
                        type=str,
                        help="Write isbn book code")
    parser.add_argument("pages_number",
                        type=int,
                        help="Write pages number")
    parser.add_argument("link",
                        type=str,
                        help="Write pic link")
    parser.add_argument("lan",
                        type=str,
                        help="Write language: pl")

    def post(self):
        try:
            args = self.parser.parse_args()
        except:
            pass
        book = Book(**args)
        if book.save_to_db():
            return {'messege': 'Book created successfully'}
        return {'message': 'Failed with adding book! There is already book with that isbn number'}, 404

    def get(self):

        books = Book.query

        if books.count() > 0:
            return [book.json() for book in books]
        return {'message': 'Item not found'}, 404


# Sample json POST content
# {
#   "title": "Bardzo",
#   "author": "Bardzo znany autor",
#   "pub_date": "2021-11-17",
#   "isbn": "9781473226155",
#   "link": "Brak",
#   "lan": "en",
#   "pages": 0
# }

class BookFilter(Resource):

    # bookrest/wiedz/sap/pl/2000-12-18/2020-12-18
    def get(self, title, author, lan, data_str, data_end):

        books = Book.query

        books = books.filter(Book.pub_date.between(data_str, data_end))

        args = {
            "title": title,
            "author": author,
            "lan": lan,
        }
        for key in args:
            if args[key] != "all":
                books = search_book(key, args[key], books)

        if books.count() > 0:
            return [book.json() for book in books]
        return {'message': 'Item not found'}, 404
