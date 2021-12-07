from tests.system.base_test import BaseTest
from app import app
import json

class TestHomme(BaseTest):
    def test_home(self):
        with self.app() as c:
            resp = c.get('/')

            self.assertEqual(resp.status_code, 200)
            # self.assertEqual()