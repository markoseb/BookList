from tests.unit.unit_base_test import UnitBaseTest
from book_list.models import Book
import datetime


class BookTest(UnitBaseTest):
    dt_string = "2020-12-18"
    format = "%Y-%m-%d"
    dt_object = datetime.datetime.strptime(dt_string, format)

    def test_create_book(self):
        book = Book("test", "testAuthor",
                    "2020-12-18",
                    9788326419935, 2137,
                    "http://books.google.com/books/content?id=c0hSAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                    "pl")
        self.assertEqual(book.title, 'test', "Problem with book title")
        self.assertEqual(book.author, 'testAuthor', "Problem with book author")
        self.assertEqual(book.pub_date, self.dt_object, "Problem with book pub_date")
        self.assertEqual(book.isbn, 9788326419935, "Problem with book isbn")
        self.assertEqual(book.pages_number, 2137, "Problem with book pages_number")
        self.assertEqual(book.link,
                         "http://books.google.com/books/content?id=c0hSAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api")
        self.assertEqual(book.lan, 'pl', "Problem with book language")

    def test_book_json(self):
        book = Book("test", "testAuthor",
                    "2020-12-18",
                    9788326419935, 2137,
                    "http://books.google.com/books/content?id=c0hSAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                    "pl")
        expected = {'title': "test",
                    'author': "testAuthor",
                    'pub_date': "2020-12-18",
                    'isbn': 9788326419935,
                    'pages_number': 2137,
                    'link': "http://books.google.com/books/content?id=c0hSAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                    'lan': "pl",
                    }
        self.assertEqual(book.json(), expected, "Book.json failed")
