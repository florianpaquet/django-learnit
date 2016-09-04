from django.db import IntegrityError
from django.test import (
    TestCase,
    TransactionTestCase)
from django.views.generic import View

from ..views.base import DocumentMixin
from ..factories import LabelledDocumentFactory
from ..models import LabelledDocument

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

    def test_get_for_document_is_none_when_missing(self):
        """Returns None when document is not labelled"""
        document = Document.objects.create()
        LabelledDocumentFactory.create(model_name='model', document=document)

        self.assertIsNone(LabelledDocument.objects.get_for_document(document, 'other'))

        document = Document.objects.create()
        self.assertIsNone(LabelledDocument.objects.get_for_document(document, 'model'))

    def test_get_for_document(self):
        """Returns the LabelledDocument"""
        document = Document.objects.create()
        labelled_document = LabelledDocumentFactory.create(
            model_name='model', document=document)

        self.assertEqual(
            LabelledDocument.objects.get_for_document(document, 'model'),
            labelled_document)

    def test_update_or_create_for_document_is_created(self):
        """LabelledDocument is created when missing"""
        document = Document.objects.create()
        obj, created = LabelledDocument.objects.update_or_create_for_document(
            document, 'model', 'foobar')

        self.assertTrue(created)
        self.assertEqual(obj.value, 'foobar')

    def test_update_or_create_for_document_is_updated(self):
        """LabelledDocument is updated when existing"""
        document = Document.objects.create()
        labelled_document = LabelledDocumentFactory.create(
            document=document, model_name='model', value='oldvalue')

        obj, created = LabelledDocument.objects.update_or_create_for_document(
            document, 'model', 'newvalue')

        self.assertFalse(created)
        self.assertEqual(obj, labelled_document)
        self.assertEqual(obj.value, 'newvalue')


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
