from django.test import TestCase
from django.views.generic import (
    View,
    TemplateView)

from ..views.base import (
    LearningModelMixin,
    DocumentMixin)
from ..views.classifier import (
    ClassifierModelMixin)
from ..forms import (
    SingleLabelClassifierForm,
    MultiLabelClassifierForm)

from .learnit import (
    TestModel,
    TestSingleLabelClassifierModel,
    TestMultiLabelClassifierModel)
from .models import Document


class LearningModelMixinTestView(LearningModelMixin, View):
    pass


class LearningModelMixinTestCase(TestCase):

    def setUp(self):
        self.view = LearningModelMixinTestView(kwargs={
            'name': TestModel.get_name()
        })

    def test_get_learning_model(self):
        """Learning model is returned"""
        self.assertEqual(self.view.get_learning_model().__class__, TestModel)

# ---


class DocumentMixinTestView(DocumentMixin, View):
    pass


class DocumentMixinTestCase(TestCase):

    def setUp(self):
        self.view = DocumentMixinTestView()

    def test_get_queryset(self):
        """Returns the learning model queryset"""
        self.view.learning_model = TestModel()
        self.assertEqual(self.view.get_queryset().model, Document)

# ---


class ClassifierModelMixinTestView(ClassifierModelMixin, TemplateView):
    pass


class ClassifierModelMixinTestCase(TestCase):

    def setUp(self):
        self.view = ClassifierModelMixinTestView()

    def test_get_classes(self):
        """Returns the classifier classes"""
        self.view.learning_model = TestSingleLabelClassifierModel()
        self.assertEqual(self.view.get_classes(), TestSingleLabelClassifierModel.classes)

    def test_get_context_data(self):
        """Adds classifier context data"""
        # Single label
        self.view.learning_model = TestSingleLabelClassifierModel()
        context = self.view.get_context_data()

        self.assertEqual(context['classes'], TestSingleLabelClassifierModel.classes)
        self.assertFalse(context['multilabel'])

        # Multi label
        self.view.learning_model = TestMultiLabelClassifierModel()
        context = self.view.get_context_data()

        self.assertEqual(context['classes'], TestMultiLabelClassifierModel.classes)
        self.assertTrue(context['multilabel'])

    def test_get_form_class(self):
        """Returns the form class matchin multilabel attribute"""
        # Single label
        self.view.learning_model = TestSingleLabelClassifierModel()
        self.assertEqual(self.view.get_form_class(), SingleLabelClassifierForm)

        # Multi label
        self.view.learning_model = TestMultiLabelClassifierModel()
        self.assertEqual(self.view.get_form_class(), MultiLabelClassifierForm)
