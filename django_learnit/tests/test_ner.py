from django.core.urlresolvers import reverse
from django.test import (
    TestCase,
    RequestFactory)
from django.views.generic import FormView

from ..forms.classifier import SingleLabelClassifierForm
from ..learning.ner import NamedEntityRecognizerModel
from ..views.ner import NamedEntityRecognizerModelLabellingMixin
from ..models import LabelledDocument

from .factories import LabelledDocumentFactory
from .models import Document
from .learning_models import TestNamedEntityRecognizerModel


# -- Learning models

class NamedEntityRecognizerModelTestCase(TestCase):

    class NERModel(NamedEntityRecognizerModel):
        classes = (
            ('TEST', 'test'),
        )

    def setUp(self):
        self.model = self.NERModel()

    def test_default_outside_class_is_added_to_classes(self):
        """Outside class is added"""
        expected = (
            ('O', 'OUTSIDE'),
            ('TEST', 'test')
        )
        self.assertEqual(self.model.get_classes(), expected)

    def test_specific_outside_class_is_added_to_classes(self):
        """Specific outside class is added"""
        self.model.outside_class = 'NOPE'
        self.model.outside_class_display = 'Nope'

        expected = (
            ('NOPE', 'Nope'),
            ('TEST', 'test')
        )

        self.assertEqual(self.model.get_classes(), expected)

    def test_get_tokens_raise_default(self):
        """Raise NotImplementedError by default"""
        with self.assertRaises(NotImplementedError):
            self.model.get_tokens(None)


# -- Mixins

class NamedEntityRecognizerModelLabellingMixinTestView(
        NamedEntityRecognizerModelLabellingMixin, FormView):
    pass


class NamedEntityRecognizerModelLabellingMixinTestCase(TestCase):

    class NERModel(NamedEntityRecognizerModel):
        name = 'nermodel'
        classes = (
            ('LOCATION', 'Location'),
            ('DATE', 'Date')
        )

        def get_tokens(self, document):
            return document

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        self.view = NamedEntityRecognizerModelLabellingMixinTestView()
        self.view.request = self.request

        self.learning_model = self.NERModel()
        self.view.learning_model = self.learning_model

    def test_get_context_data(self):
        """Adds tokens and classes to the context"""
        self.view.tokens = ['foo', 'bar']
        context = self.view.get_context_data()

        self.assertEqual(context['classes'], self.learning_model.get_classes())
        self.assertEqual(context['tokens'], ['foo', 'bar'])

    def test_get_form_class(self):
        """Returns a SingleLabelClassifierForm formset"""
        self.view.tokens = []
        form_class = self.view.get_form_class()

        self.assertEqual(form_class.__name__, 'SingleLabelClassifierFormFormSet')
        self.assertEqual(form_class().form().__class__, SingleLabelClassifierForm)

    def test_get_initial_default(self):
        """Returns a list of outside labels dicts"""
        self.view.tokens = [1, 2, 3]
        initial = self.view.get_initial()
        self.assertEqual(initial, [
            {'label': 'O'},
            {'label': 'O'},
            {'label': 'O'}
        ])


# -- Functional

class NamedEntityRecognizerModelFunctionalTestCase(TestCase):

    def test_create_labelled_document(self):
        """LabelledDocument is created for new document"""
        model_name = TestNamedEntityRecognizerModel().get_name()

        document = Document.objects.create()
        self.assertFalse(LabelledDocument.objects.exists())

        url = reverse('django_learnit:document-labelling', kwargs={
            'name': model_name,
            'pk': document.pk
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        data = form.initial

        self.assertEqual(data, [
            {'label': 'O'},
            {'label': 'O'}
        ])

        data[0] = {'label': 'DAY'}

        formdata = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '2',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '2',
            'form-0-label': 'DAY',
            'form-1-label': 'O'
        }

        self.client.post(url, formdata)

        labelled_document = LabelledDocument.objects.get_for_document(
            document, model_name)

        expected_value = LabelledDocument.serialize_value(data)
        self.assertEqual(labelled_document.value, expected_value)

    def test_update_labelled_document(self):
        """Reset to outside labels list when tokens length differs"""
        model_name = TestNamedEntityRecognizerModel().get_name()

        document = Document.objects.create()
        LabelledDocumentFactory.create(
            document=document,
            model_name=model_name,
            value=LabelledDocument.serialize_value([
                {'label': 'DAY'},
                {'label': 'O'}
            ]))

        url = reverse('django_learnit:document-labelling', kwargs={
            'name': model_name,
            'pk': document.pk
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        data = form.initial

        self.assertEqual(data, [
            {'label': 'DAY'},
            {'label': 'O'}
        ])

        data[1] = {'label': 'DAY'}

        formdata = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '2',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '2',
            'form-0-label': 'DAY',
            'form-1-label': 'DAY'
        }

        self.client.post(url, formdata)

        labelled_document = LabelledDocument.objects.get_for_document(
            document, model_name)

        expected_value = LabelledDocument.serialize_value(data)
        self.assertEqual(labelled_document.value, expected_value)

