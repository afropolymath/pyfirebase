import re
import requests
import validators


class FirebaseReference(object):
    def __init__(self, connector, reference):
        self.connector = connector
        self.current = reference

    def child(self, reference):
        if not FirebaseReference.is_valid(reference):
            raise ValueError("Invalid reference value")
        self.current = self.current + "/" + reference
        return self

    def add(self, payload):
        result = requests.post(self.current_url, data=payload)
        if result.status_code == 200:
            return result.json()

    def get(self):
        result = requests.get(self.current_url)
        if result.status_code == 200:
            return result.json()

    def set(self, payload):
        result = requests.put(self.current_url, data=payload)
        if result.status_code == 200:
            return result.json()

    def update(self, payload):
        result = requests.patch(self.current_url, data=payload)
        if result.status_code == 200:
            return result.json()

    def delete(self):
        result = requests.delete(self.current_url)
        if result.status_code == 200:
            return result.json()

    @staticmethod
    def is_valid(reference):
        pattern = re.compile('[a-zA-Z0-9]+(\\[a-zA-Z0-9]+)*')
        matches = pattern.match(reference)
        if matches:
            return True
        return False

    @property
    def current_url(self):
        base = self.connector.FIREBASE_URL
        url = "{}/{}.json".format(base, self.current)
        return url


class Firebase(object):
    FIREBASE_URL = None

    def __new__(cls, *args):
        if len(args) == 1:
            if Firebase.is_valid_firebase_url(args[0]):
                return super(Firebase, cls).__new__(cls)
        return None

    def __init__(self, url):
        self.FIREBASE_URL = url

    @staticmethod
    def is_valid_firebase_url(url):
        if validators.url(url):
            pattern = re.compile('.+firebaseio(-demo)?\.com$')
            matches = pattern.match(url)
            if matches:
                return True
        return False

    def ref(self, reference):
        if FirebaseReference.is_valid(reference):
            return FirebaseReference(self, reference)
