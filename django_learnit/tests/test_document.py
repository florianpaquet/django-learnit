import json

from django import forms
from django.db import IntegrityError
from django.http import HttpRequest
from django.test import (
    RequestFactory,
    TestCase,
    TransactionTestCase)
from django.views.generic import (
    View,
    FormView)

from ..views.base import (
    DocumentMixin,
    LabelledDocumentFormMixin,
    BaseLearningModelLabellingView)
from ..models import LabelledDocument

from .factories import LabelledDocumentFactory
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

    def test_serialize_value(self):
        """Value is serialized as a JSON object"""
        value = [['foo', 'bar', 'baz'], {'hello': 'world'}]
        self.assertEqual(
            LabelledDocument.serialize_value(value), json.dumps(value))

    def test_invalid_json_value(self):
        """Returns an empty dict when json value is invalid"""
        document = Document.objects.create()
        labelled_document = LabelledDocumentFactory.create(
            document=document, value="{{{foobar]")

        self.assertEqual(labelled_document.deserialize_value(), {})

    def test_json_value(self):
        """JSON value is deserialized"""
        value = {
            'foo': 'bar',
            'hello': ['world', '!']
        }

        document = Document.objects.create()
        labelled_document = LabelledDocumentFactory.create(
            document=document, value=json.dumps(value))

        self.assertEqual(labelled_document.deserialize_value(), value)


# -- Managers

class LabelledDocumentManagerTestCase(TestCase):

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


class LabelledDocumentFormMixinTestView(LabelledDocumentFormMixin, FormView):
    success_url = '/'


class LabelledDocumentFormMixinTestCase(TestCase):

    def setUp(self):
        self.document = Document.objects.create()
        self.learning_model = TestModel()

        self.view = LabelledDocumentFormMixinTestView()
        self.view.object = self.document
        self.view.learning_model = self.learning_model

    def test_get_initial_without_labelled_document(self):
        """Initial data is empty"""
        self.assertEqual(self.view.get_initial(), {})

    def test_get_initial(self):
        """Initial data is the LabelledDocument JSON value"""
        value = {
            'foo': 'bar',
            'hello': ['world']
        }

        LabelledDocumentFactory.create(
            document=self.document,
            model_name=self.learning_model.get_name(),
            value=json.dumps(value))

        self.assertDictEqual(self.view.get_initial(), value)

    def test_labelled_document_is_created_when_form_valid(self):
        """LabelledDocument is created when missing"""
        form = forms.Form()
        form.cleaned_data = {
            'foo': 'bar'
        }

        self.view.form_valid(form)

        labelled_document = LabelledDocument.objects.get_for_document(
            self.document, self.learning_model.get_name())
        self.assertEqual(labelled_document.deserialize_value(), form.cleaned_data)


# -- Views

class BaseLearningModelLabellingViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.document = Document.objects.create()

    def setup_view(self, view, request, **kwargs):
        view.request = request
        view.kwargs = kwargs
        view.form_class = forms.Form
        view.template_name = ''
        view.success_url = '/'
        return view

    def test_get_sets_attributes(self):
        """GET sets learning model and object attributes"""
        request = self.factory.get('/')

        view = self.setup_view(
            BaseLearningModelLabellingView(),
            request,
            name=TestModel.get_name(),
            pk=self.document.pk)

        view.get(request)

        self.assertEqual(view.learning_model.__class__, TestModel)
        self.assertEqual(view.object, self.document)

    def test_post_sets_attributes(self):
        """POST sets learning model and object attributes"""
        request = self.factory.post('/')

        view = self.setup_view(
            BaseLearningModelLabellingView(),
            request,
            name=TestModel.get_name(),
            pk=self.document.pk)

        view.post(request)

        self.assertEqual(view.learning_model.__class__, TestModel)
        self.assertEqual(view.object, self.document)
