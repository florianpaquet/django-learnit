from django.test import (
    TestCase,
    RequestFactory)
from django.views.generic import (
    TemplateView,
    FormView)

from ..exceptions import ImproperlyConfigured
from ..forms.classifier import (
    SingleLabelClassifierForm,
    MultiLabelClassifierForm)
from ..learning.classifier import ClassifierModel
from ..views.classifier import ClassifierModelLabellingMixin

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

class ClassifierModelLabellingMixinTestView(ClassifierModelLabellingMixin, TemplateView):
    pass


class ClassifierModelLabellingMixinTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = ClassifierModelLabellingMixinTestView()

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

    def test_form_kwargs(self):
        """Classes are added to the form kwargs"""
        request = self.factory.get('/')
        learning_model = TestSingleLabelClassifierModel()

        class TestView(ClassifierModelLabellingMixin, FormView):
            pass

        view = TestView(request=request, learning_model=learning_model)
        kwargs = view.get_form_kwargs()

        self.assertEqual(kwargs['classes'], learning_model.get_classes())
