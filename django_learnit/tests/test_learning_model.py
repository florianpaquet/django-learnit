from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import (
    TestCase,
    RequestFactory)
from django.views.generic import TemplateView

from ..exceptions import ImproperlyConfigured
from ..learning.base import LearningModel
from ..views.base import LearningModelMixin
from ..views.detail import LearningModelDetailView

from .factories import LabelledDocumentFactory
from .models import Document
from .learning_models import TestModel


class LearningModelTestCase(TestCase):

    def test_get_name_raises_when_not_set(self):
        """Raise exception when name is not set"""
        class TestModel(LearningModel):
            pass

        with self.assertRaises(ImproperlyConfigured):
            TestModel.get_name()

    def test_get_name_raises_when_not_a_string(self):
        """Raise exception when name is not a string"""
        class TestModel(LearningModel):
            name = 1 + 1

        with self.assertRaises(ImproperlyConfigured):
            TestModel.get_name()

    def test_get_name_raises_when_empty_string(self):
        """Raise exception when name is an empty string"""
        class TestModel(LearningModel):
            name = '  '

        with self.assertRaises(ImproperlyConfigured):
            TestModel.get_name()

    def test_get_name(self):
        """Get the model name"""
        class TestModel(LearningModel):
            name = 'modelname'

        self.assertEqual(TestModel.get_name(), 'modelname')

    def test_get_queryset_raises_when_not_set(self):
        """Raise exception when queryset is not set"""
        class TestModel(LearningModel):
            pass

        with self.assertRaises(ImproperlyConfigured):
            TestModel().get_queryset()

    def test_get_queryset(self):
        """Get the document queryset"""
        class TestModel(LearningModel):
            queryset = Document.objects.all()

        self.assertEqual(TestModel().get_queryset().model, Document)

    def test_learning_model_type(self):
        class TestModel(LearningModel):
            pass

        self.assertFalse(TestModel().is_classifier())

    def test_get_random_unlabelled_document_is_none_when_nothing_left(self):
        """Returns None when everything is labelled"""
        class TestModel(LearningModel):
            name = 'testmodel'
            queryset = Document.objects.all()

        document = Document.objects.create()

        LabelledDocumentFactory.create(
            document=document, model_name=TestModel.get_name(), value='foo')
        LabelledDocumentFactory.create(
            document=document, model_name='othermodel', value='foo')

        self.assertIsNone(TestModel().get_random_unlabelled_document())

    def test_get_random_unlabelled_document(self):
        """Returns a random unlabelled document"""
        class TestModel(LearningModel):
            name = 'testmodel'
            queryset = Document.objects.all()

        document1 = Document.objects.create()
        document2 = Document.objects.create()
        document3 = Document.objects.create()

        LabelledDocumentFactory.create(
            document=document1, model_name=TestModel.get_name(), value='foo')
        LabelledDocumentFactory.create(
            document=document2, model_name='othermodel', value='foo')

        self.assertIn(
            TestModel().get_random_unlabelled_document().pk,
            [document2.pk, document3.pk])


# -- Mixins

class LearningModelMixinTestView(LearningModelMixin, TemplateView):
    pass


class LearningModelMixinTestCase(TestCase):

    def setUp(self):
        self.view = LearningModelMixinTestView(kwargs={
            'name': TestModel.get_name()
        })

    def test_get_learning_model(self):
        """Learning model is returned"""
        self.assertEqual(self.view.get_learning_model().__class__, TestModel)

    def test_get_learning_model_raises_when_model_is_not_registered(self):
        """Raise HTTP 404 when model doesn't exist"""
        view = LearningModelMixinTestView(kwargs={
            'name': 'iamnotregistered'
        })

        with self.assertRaises(Http404):
            self.assertEqual(view.get_learning_model())

    def test_get_context_data(self):
        """Adds learning model data in the context"""
        self.view.learning_model = TestModel()
        context = self.view.get_context_data()

        self.assertEqual(
            context['learning_model'], self.view.learning_model)
        self.assertEqual(
            context['learning_model_name'], self.view.learning_model.get_name())

    def test_get_random_unlabelled_document_url_when_nothing_left(self):
        """Detail view when nothing is left"""
        self.view.learning_model = TestModel()

        document = Document.objects.create()
        LabelledDocumentFactory.create(
            document=document, model_name=self.view.learning_model.get_name())

        expected_url = reverse('django_learnit:learning-model-detail', kwargs={
            'name': self.view.learning_model.get_name()
        })

        self.assertEqual(self.view.get_random_unlabelled_document_url(), expected_url)

    def test_get_random_unlabelled_document_url(self):
        """Document labelling URL is returned"""
        self.view.learning_model = TestModel()

        document1 = Document.objects.create()
        document2 = Document.objects.create()

        LabelledDocumentFactory.create(
            document=document1, model_name=self.view.learning_model.get_name())

        expected_url = reverse('django_learnit:document-labelling', kwargs={
            'name': self.view.learning_model.get_name(),
            'pk': document2.pk
        })

        self.assertEqual(self.view.get_random_unlabelled_document_url(), expected_url)


# -- Views

class LearningModelDetailViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = LearningModelDetailView()

    def test_get_template_names(self):
        """Adds a learning model specific template name"""
        class TestModel(LearningModel):
            name = 'foobarmodel'

        self.view.learning_model = TestModel()
        template_names = self.view.get_template_names()

        self.assertEqual(
            template_names,
            [
                'django_learnit/learning_models/foobarmodel_detail.html',
                'django_learnit/learning_models/detail.html'
            ]
        )

    def test_get_sets_attributes(self):
        """GET method sets view attributes"""
        request = self.factory.get('/')

        self.view.kwargs = {
            'name': TestModel.get_name()
        }
        self.view.request = request

        self.view.get(request)
        self.assertEqual(self.view.learning_model.__class__, TestModel)
