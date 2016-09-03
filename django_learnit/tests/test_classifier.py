from django.test import TestCase
from django.views.generic import TemplateView

from ..exceptions import ImproperlyConfigured
from ..forms import (
    SingleLabelClassifierForm,
    MultiLabelClassifierForm)
from ..learning.classifier import ClassifierModel
from ..views.classifier import ClassifierModelMixin

from .learning_models import (
    TestSingleLabelClassifierModel,
    TestMultiLabelClassifierModel)


# -- Model

class ClassifierModelTestCase(TestCase):

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


# -- Forms

class ClassifierFormTestCase(TestCase):

    def test_label_choices(self):
        """Label choices are set during form initialization"""
        test_classes = (
            (0, 'No'),
            (1, 'Yes')
        )

        form = SingleLabelClassifierForm(classes=test_classes)
        self.assertEqual(tuple(form.fields['label'].choices), test_classes)

        form = MultiLabelClassifierForm(classes=test_classes)
        self.assertEqual(tuple(form.fields['label'].choices), test_classes)


# -- Mixins

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
