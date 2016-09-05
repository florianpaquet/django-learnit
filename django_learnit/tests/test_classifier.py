from django.core.urlresolvers import reverse
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
from ..models import LabelledDocument
from ..views.classifier import ClassifierModelLabellingMixin

from .factories import LabelledDocumentFactory
from .learning_models import (
    TestSingleLabelClassifierModel,
    TestMultiLabelClassifierModel)
from .models import Document


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

    def test_predict_raises_default(self):
        """Raise NotImplementedError by default"""
        with self.assertRaises(NotImplementedError):
            self.assertIsNone(TestSingleLabelClassifierModel().predict(None))


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


# -- Functional

class ClassifierModelFunctionalTestCase(TestCase):

    def test_create_labelled_document(self):
        """LabelledDocument is created for new document"""
        model_name = TestSingleLabelClassifierModel.get_name()

        document = Document.objects.create()
        self.assertFalse(LabelledDocument.objects.exists())

        url = reverse('django_learnit:document-labelling', kwargs={
            'name': model_name,
            'pk': document.pk
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertIsInstance(form, SingleLabelClassifierForm)

        data = form.initial
        data['label'] = '1'

        self.client.post(url, data)

        labelled_document = LabelledDocument.objects.get_for_document(
            document, model_name)

        expected_value = LabelledDocument.serialize_value({
            'label': '1'
        })

        self.assertEqual(labelled_document.value, expected_value)

    def test_update_labelled_document(self):
        """LabelledDocument is updated when existing"""
        model_name = TestMultiLabelClassifierModel.get_name()

        document = Document.objects.create()

        labelled_document = LabelledDocumentFactory.create(
            document=document,
            model_name=model_name,
            value=LabelledDocument.serialize_value({
                'label': ['1', '0']
            }))
        self.assertEqual(LabelledDocument.objects.count(), 1)

        url = reverse('django_learnit:document-labelling', kwargs={
            'name': model_name,
            'pk': document.pk
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertIsInstance(form, MultiLabelClassifierForm)

        data = form.initial
        data['label'] = ['1']

        self.client.post(url, data)
        self.assertEqual(LabelledDocument.objects.count(), 1)

        expected_value = LabelledDocument.serialize_value({
            'label': ['1']
        })

        labelled_document = LabelledDocument.objects.get(pk=labelled_document.pk)
        self.assertEqual(labelled_document.value, expected_value)
