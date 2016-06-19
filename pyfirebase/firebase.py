import re
import json
import socket
import requests
import threading
from decorators import validate_payload, parse_results
from sseclient import SSEClient


class FirebaseEvents(object):
    CHILD_CHANGED = 0
    CHILD_ADDED = 2
    CHILD_DELETED = 1

    @staticmethod
    def id(event_name):
        ev = None
        mapping = {
            'child_changed': FirebaseEvents.CHILD_CHANGED,
            'child_added': FirebaseEvents.CHILD_ADDED,
            'child_deleted': FirebaseEvents.CHILD_DELETED
        }
        try:
            ev = mapping.get(event_name)
        finally:
            return ev


class ClosableSSEClient(SSEClient):
    def __init__(self, *args, **kwargs):
        self.should_connect = True
        super(ClosableSSEClient, self).__init__(*args, **kwargs)

    def _connect(self):
        if self.should_connect:
            super(ClosableSSEClient, self)._connect()
        else:
            raise StopIteration()

    def close(self):
        self.should_connect = False
        self.retry = 0
        self.resp.raw._fp.fp._sock.shutdown(socket.SHUT_RDWR)
        self.resp.raw._fp.fp._sock.close()


class EventSourceClient(threading.Thread):
    def __init__(self, url, event_name, callback):
        self.url = url
        self.event_name = event_name
        self.callback = callback
        super(EventSourceClient, self).__init__()

    def run(self):
        try:
            self.sse = ClosableSSEClient(self.url)
            for msg in self.sse:
                event = msg.event
                if event is not None and event in ('put', 'patch'):
                    response = json.loads(msg.data)
                    if response is not None:
                        # Default to CHILD_CHANGED event
                        occurred_event = FirebaseEvents.CHILD_CHANGED
                        if response['data'] is None:
                            occurred_event = FirebaseEvents.CHILD_DELETED

                        # Get the event I'm trying to listen to
                        ev = FirebaseEvents.id(self.event_name)
                        if occurred_event == ev or ev == FirebaseEvents.CHILD_CHANGED:
                            self.callback(event, response)
        except socket.error:
            pass


class FirebaseReference(object):
    def __new__(cls, *args):
        if len(args) == 2:
            connector = args[0]
            if isinstance(connector, Firebase):
                if args[1] is None or FirebaseReference.is_valid(args[1]):
                    return super(FirebaseReference, cls).__new__(cls)
        return None

    def __init__(self, connector, reference=None):
        self.connector = connector
        self.current = reference or ''

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
        return "{}/{}.json".format(base, self.current)

    def patch_url(self):
        if self.current == '':
            return self.current_url
        base = self.connector.FIREBASE_URL
        return "{}/{}/.json".format(base, self.current)

    def on(self, event_name, **kwargs):
        url = self.patch_url()
        callback = kwargs.get('callback', None)
        if event_name is None or callback is None:
            raise AttributeError(
                'No callback parameter provided'
            )
        if FirebaseEvents.id(event_name) is None:
            raise AttributeError(
                'Unsupported event'
            )
        # Start Event Source Listener on this ref on a new thread
        self.client = EventSourceClient(url, event_name, callback)
        self.client.start()
        return True

    def off(self):
        try:
            # Close Event Source Listener
            self.client.sse.close()
            self.client.join()
            return True
        except Exception:
            print "Error while trying to end the thread. Try again!"


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
            r'^https://[a-zA-Z0-9_\-]+\.firebaseio(-demo)?\.com/?$'
        )
        matches = pattern.match(url)
        if matches:
            return True
        return False

    def ref(self, reference=None):
        ref = FirebaseReference(self, reference)
        if ref is None:
            raise Exception(
                "Something went wrong when trying to create your ref"
            )
        return ref
