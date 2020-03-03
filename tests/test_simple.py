from django.test import TestCase

class SimpleTest(TestCase):
    def setUp(self):
        pass
    def test_true(self):
        self.assertTrue(True)

