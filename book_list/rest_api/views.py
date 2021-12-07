from flask_restful import Resource, reqparse
from book_list.models import Book
from book_list.core.views import search_book


class BookRest(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("title",
                        type=str,
                        help="Write title")
    parser.add_argument("author",
                        type=str,
                        help="Write author name")
    parser.add_argument("lan",
                        type=str,
                        help="Write language like en, pl")
    parser.add_argument("data_str",
                        type=str,
                        help="Write start date like : 2020-12-18")
    parser.add_argument("data_end",
                        type=str,
                        help="Write end date like : 2020-12-18")

    def post(self):

        books = Book.query
        try:
            args = self.parser.parse_args()
        except:
            return {"Sample json parameters": {
                "title": "Wiedzmin",
                "data_str": "2020-12-18",
                "data_end": "2020-12-18",
                "author": "Andrzej Sapkowski"}}, 404

        if args['data_str'] and args['data_end']:
            try:
                books = books.filter(Book.pub_date.between(args['data_str'], args['data_end']))
            except:
                pass

        for key in args:
            if args[key] and key not in ['data_str', 'data_end']:
                books = search_book(key, args[key], books)

        if books:
            return [book.json() for book in books]
        return {'message': 'Item not found'}, 404

    def get(self):

        books = Book.query
        if books:
            return [book.json() for book in books]
        return {'message': 'Item not found'}, 404
