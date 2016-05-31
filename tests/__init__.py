import unittest

from .test_firebase import TestFirebase


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFirebase))
    return suite
