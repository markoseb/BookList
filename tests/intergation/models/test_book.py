from book_list.models import Book
from tests.base_test import BaseTest


class BookTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            book = Book("test", "testAuthor",
                        "2020-12-18",
                        9788326419935, 2137,
                        "http://books.google.com/books/content?id=c0hSAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                        "pl")
            self.assertIsNone(Book.find_by_isbn(9788326419935),
                              f"Found an book with title {book.title}, but expected not to")

            book.save_to_db()

            self.assertIsNotNone(Book.find_by_isbn(9788326419935),
                                 f" Didn't Found an book with title {book.title}, but expected to")

            book.delete_from_db()

            self.assertIsNone(Book.find_by_isbn(9788326419935))
