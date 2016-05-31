import re
import requests
from functools import wraps


def validate_payload(func):
    @wraps(func)
    def func_wrapper(instance, payload):
        native_types = [bool, int, float, str, list, tuple, dict]
        if type(payload) not in native_types:
            raise ValueError("Invalid payload specified")
        return func(instance, payload)
    return func_wrapper


def parse_results(func):
    @wraps(func)
    def func_wrapper(instance, *args, **kwargs):
        results = func(instance, *args, **kwargs)
        if results.status_code == 200:
            return results.json()
        else:
            results.raise_for_status()
    return func_wrapper


class FirebaseReference(object):
    def __new__(cls, *args):
        if len(args) == 2:
            connector = args[0]
            if isinstance(connector, Firebase):
                print args
                if FirebaseReference.is_valid(args[1]):
                    return super(FirebaseReference, cls).__new__(cls)
        return None

    def __init__(self, connector, reference):
        self.connector = connector
        self.current = reference

    def child(self, reference):
        if not FirebaseReference.is_valid(reference):
            raise ValueError("Invalid reference value")
        self.current = "{}/{}".format(self.current, reference)
        return self

    @parse_results
    @validate_payload
    def push(self, payload):
        return requests.post(self.current_url, json=payload)

    @parse_results
    def get(self):
        return requests.get(self.current_url)

    @parse_results
    @validate_payload
    def set(self, payload):
        return requests.put(self.current_url, json=payload)

    @parse_results
    @validate_payload
    def update(self, payload):
        return requests.patch(self.current_url, json=payload)

    @parse_results
    def delete(self):
        return requests.delete(self.current_url)

    @staticmethod
    def is_valid(reference):
        pattern = re.compile('^[a-zA-Z0-9_-]+(\/[a-zA-Z0-9_-]+)*$')
        matches = pattern.match(reference)
        if matches:
            return True
        return False

    @property
    def current_url(self):
        base = self.connector.FIREBASE_URL
        url = "{}/{}.json".format(base, self.current)
        return url

    def patch_url(self):
        base = self.connector.FIREBASE_URL
        url = "{}/{}/.json".format(base, self.current)
        return url


class Firebase(object):
    FIREBASE_URL = None

    def __new__(cls, *args):
        if len(args) == 1:
            if Firebase.is_valid_firebase_url(args[0]):
                return super(Firebase, cls).__new__(cls)
        return None

    def __init__(self, url):
        self.FIREBASE_URL = url.strip('/')

    @staticmethod
    def is_valid_firebase_url(url):
        pattern = re.compile(
            r'^https://[a-zA-Z0-9\-]+\.firebaseio(-demo)?\.com/?$'
        )
        matches = pattern.match(url)
        if matches:
            return True
        return False

    def ref(self, reference):
        ref = FirebaseReference(self, reference)
        if ref is None:
            raise Exception(
                "Something went wrong when trying to create your ref"
            )
        return ref
