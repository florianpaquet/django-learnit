from django.test import TestCase

from ..exceptions import ImproperlyConfigured
from ..learning.classifier import ClassifierModel


class ClassifierTestCase(TestCase):

    def test_learning_model_type(self):
        class TestModel(ClassifierModel):
            pass

        self.assertTrue(TestModel().is_classifier())

    def test_get_classes_raises_when_empty(self):
        """Raise exception when no classes"""
        class TestClassifier(ClassifierModel):
            pass

        with self.assertRaises(ImproperlyConfigured):
            TestClassifier().get_classes()

    def test_get_classes(self):
        """Returns classifier classes"""
        test_classes = (
            (0, 'No'),
            (1, 'Yes')
        )

        class TestClassifier(ClassifierModel):
            classes = test_classes

        self.assertEqual(TestClassifier().get_classes(), test_classes)
