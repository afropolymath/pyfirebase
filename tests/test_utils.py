from unittest import TestCase
from pyfirebase import Firebase, FirebaseReference

class TestUtils(TestCase):
    def test_valid_firebase_url(self):
        test_urls = [
            'https://validurl.firebaseio.com',
            'https://anothervalidurl.firebaseio.com/',
            'https://another-validurl98.firebaseio.com/'
        ]
        for url in test_urls:
            self.assertTrue(Firebase.is_valid_firebase_url(url))
