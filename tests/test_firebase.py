import mock
from mock import MagicMock
from unittest import TestCase
from pyfirebase import Firebase, FirebaseReference

TEST_FIREBASE_URL = 'https://samplechat.firebaseio-demo.com'


class TestFirebase(TestCase):
    def setUp(self):
        self.firebase = Firebase(TEST_FIREBASE_URL)
        self.assertIsInstance(self.firebase, Firebase)

    def test_ref(self):
        node_ref = self.firebase.ref('test_ref')
        self.assertIsInstance(node_ref, FirebaseReference)
        self.assertEqual(node_ref.current, 'test_ref')

    def test_child(self):
        node_ref = self.firebase.ref('test_ref')
        self.assertEqual(node_ref.current, 'test_ref')
        child_ref = node_ref.child('test_child_ref')
        self.assertEqual(child_ref.current, 'test_ref/test_child_ref')

    def test_current_url_property(self):
        node_ref = self.firebase.ref('test_ref')
        self.assertEqual(node_ref.current_url, "{}/{}.json".format(
            TEST_FIREBASE_URL,
            'test_ref')
        )

    @mock.patch('requests.get')
    def test_get_event(self, mock_requests_get):
        node_ref = self.firebase.ref('test_ref')
        results = node_ref.get()
        self.assertTrue(mock_requests_get.called)
        mock_requests_get.assert_called_with(node_ref.current_url)

    @mock.patch('requests.put')
    def test_set_event(self, mock_requests_put):
        node_ref = self.firebase.ref('test_ref')
        result = node_ref.set('val')
        self.assertTrue(mock_requests_put.called)
        mock_requests_put.assert_called_with(node_ref.current_url, json='val')

    @mock.patch('requests.post')
    def test_push_event(self, mock_requests_post):
        node_ref = self.firebase.ref('test_ref')
        result = node_ref.push('val')
        self.assertTrue(mock_requests_post.called)
        mock_requests_post.assert_called_with(node_ref.current_url, json='val')

    @mock.patch('requests.delete')
    def test_delete_event(self, mock_requests_delete):
        node_ref = self.firebase.ref('test_ref')
        result = node_ref.delete()
        self.assertTrue(mock_requests_delete.called)
        mock_requests_delete.assert_called_with(node_ref.current_url)
