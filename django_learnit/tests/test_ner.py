from django.test import TestCase

from ..learning.ner import NamedEntityRecognizerModel


# -- Learning models

class NamedEntityRecognizerModelTestCase(TestCase):

    def test_get_tokens_raise_default(self):
        """Raise NotImplementedError by default"""
        with self.assertRaises(NotImplementedError):
            NamedEntityRecognizerModel().get_tokens(None)
