from django.db import IntegrityError
from django.test import (
    TestCase,
    TransactionTestCase)
from django.views.generic import View

from ..views.base import DocumentMixin
from ..factories import LabelledDocumentFactory

from .learning_models import TestModel
from .models import Document


# -- Models

class LabelledDocumentModelTestCase(TransactionTestCase):

    def test_uniqueness(self):
        """Only one LabelledDocument instance per document and learning model"""
        document = Document.objects.create()

        LabelledDocumentFactory.create(model_name='model1', document=document)

        with self.assertRaises(IntegrityError):
            LabelledDocumentFactory.create(model_name='model1', document=document)

        self.assertTrue(
            LabelledDocumentFactory.create(model_name='model2', document=document))


# -- Mixins

class DocumentMixinTestView(DocumentMixin, View):
    pass


class DocumentMixinTestCase(TestCase):

    def setUp(self):
        self.view = DocumentMixinTestView()

    def test_get_queryset(self):
        """Returns the learning model queryset"""
        self.view.learning_model = TestModel()
        self.assertEqual(self.view.get_queryset().model, Document)
