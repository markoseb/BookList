import json

from book_list.models import Book
from tests.base_test import BaseTest


class BookFilterTest(BaseTest):
    data = {
        "title": "New",
        "author": "Bardzo znany autor",
        "pub_date": "2020-11-17",
        "isbn": "9721473226155",
        "link": "Brak",
        "lan": "en",
        "pages_number": 0
    }

    def test_filter_book(self):
        with self.app() as c:
            Book(**self.data).save_to_db()
            resp = c.get('/bookfilter/New/Bardzo_znany_autor/en/2000-12-18/2020-12-18')

            self.assertListEqual([self.data],
                                 json.loads(resp.data))

    def test_filter_title_book(self):
        with self.app() as c:
            Book(**self.data).save_to_db()
            resp = c.get('/bookfilter/New/all/all/2000-12-18/2020-12-18')

            self.assertListEqual([self.data],
                                 json.loads(resp.data))

    def test_filter_author_book(self):
        with self.app() as c:
            Book(**self.data).save_to_db()
            resp = c.get('/bookfilter/all/Bardzo_znany_autor/all/2000-12-18/2020-12-18')

            self.assertListEqual([self.data],
                                 json.loads(resp.data))

    def test_filter_author_book(self):
        with self.app() as c:
            Book(**self.data).save_to_db()
            resp = c.get('/bookfilter/all/all/en/2000-12-18/2020-12-18')

            self.assertListEqual([self.data],
                                 json.loads(resp.data))

    def test_filter_title_not_found(self):
        with self.app() as c:
            data = {
                "title": "New",
                "author": "Bardzo znany autor",
                "pub_date": "2020-11-17",
                "isbn": "9721473226155",
                "link": "Brak",
                "lan": "en",
                "pages_number": 0
            }
            Book(**data).save_to_db()
            resp = c.get('/bookfilter/Nieznany/Bardzo_znany_autor/en/2000-12-18/2020-12-18')

            self.assertDictEqual({'message': 'Item not found'},
                                 json.loads(resp.data))

    def test_filter_author_not_found(self):
        with self.app() as c:
            data = {
                "title": "New",
                "author": "Bardzo znany autor",
                "pub_date": "2020-11-17",
                "isbn": "9721473226155",
                "link": "Brak",
                "lan": "en",
                "pages_number": 0
            }
            Book(**data).save_to_db()
            resp = c.get('/bookfilter/New/Andrzej/en/2000-12-18/2020-12-18')

            self.assertDictEqual({'message': 'Item not found'},
                                 json.loads(resp.data))

    def test_filter_date_not_found(self):
        with self.app() as c:
            data = {
                "title": "New",
                "author": "Bardzo znany autor",
                "pub_date": "2000-11-17",
                "isbn": "9721473226155",
                "link": "Brak",
                "lan": "en",
                "pages_number": 0
            }
            Book(**data).save_to_db()
            resp = c.get('/bookfilter/New/Bardzo/en/2001-12-18/2020-12-18')

            self.assertDictEqual({'message': 'Item not found'},
                                 json.loads(resp.data))

    def test_filter_language_not_found(self):
        with self.app() as c:
            data = {
                "title": "New",
                "author": "Bardzo znany autor",
                "pub_date": "2002-11-17",
                "isbn": "9721473226155",
                "link": "Brak",
                "lan": "en",
                "pages_number": 0
            }
            Book(**data).save_to_db()
            resp = c.get('/bookfilter/New/Bardzo/pl/2001-12-18/2020-12-18')

            self.assertDictEqual({'message': 'Item not found'},
                                 json.loads(resp.data))
