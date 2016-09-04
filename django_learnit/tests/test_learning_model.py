from django.test import TestCase
from django.views.generic import TemplateView

from ..exceptions import ImproperlyConfigured
from ..learning.base import LearningModel
from ..views.base import LearningModelMixin

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

    def test_get_context_data(self):
        """Adds the template name in the context"""
        target_template_name = 'learning_models/%(name)s.html' % {
            'name': TestModel.get_name()
        }

        self.view.learning_model = TestModel()
        context = self.view.get_context_data()

        self.assertEqual(context['document_detail_template_name'], target_template_name)
