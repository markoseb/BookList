import json

from book_list.models import Book
from tests.base_test import BaseTest


class BookDbTest(BaseTest):
    def test_add_book(self):
        with self.app() as client:
            data = {
                "title": "Bardzo",
                "author": "Bardzo znany autor",
                "pub_date": "2021-11-17",
                "isbn": "9721473226155",
                "link": "Brak",
                "lan": "en",
                "pages": 0
            }
            resp = client.post('/bookdb', data=data)
            self.assertEqual(resp.status_code, 200)
            self.assertIsNotNone(Book.find_by_isbn(9721473226155))
            self.assertDictEqual({'messege': 'Book created successfully'},
                                 json.loads(resp.data))

    def test_add_book_duplicate(self):
        with self.app() as client:
            data = {
                "title": "New",
                "author": "Bardzo znany autor",
                "pub_date": "2020-11-17",
                "isbn": "9721473226155",
                "link": "Brak",
                "lan": "en",
                "pages": 0
            }
            client.post('/bookdb', data=data)
            resp = client.post('/bookdb', data=data)
            self.assertEqual(resp.status_code, 404)
            self.assertDictEqual({'message': 'Failed with adding book! There is already book with that isbn number'},
                                 json.loads(resp.data))

    def test_find_books(self):
        with self.app() as client:
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
            resp = client.get('/bookdb')
            self.assertEqual(resp.status_code, 200)
            self.assertListEqual([data],
                                 json.loads(resp.data))

    def test_books_not_found(self):
        with self.app() as client:
            resp = client.get('/bookdb')
            self.assertEqual(resp.status_code, 404)
            self.assertDictEqual({'message': 'Item not found'},
                                 json.loads(resp.data))
