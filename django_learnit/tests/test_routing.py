from django.test import TestCase
from django.core.urlresolvers import reverse

from ..views.classifier import ClassifierModelLabellingView

from .learning_models import (
    TestModel,
    TestSingleLabelClassifierModel)
from .models import Document


class LearningModelURLRoutingTestCase(TestCase):

    def test_labelling_non_registered_model(self):
        """HTTP 404 when model is not registered"""
        response = self.client.get(
            reverse('django_learnit:document-labelling', kwargs={
                'name': 'missingmodel',
                'pk': 1
            }))
        self.assertEqual(response.status_code, 404)

    def test_labelling_non_exising_document(self):
        """HTTP 404 when trying to label non existing document"""
        response = self.client.get(
            reverse('django_learnit:document-labelling', kwargs={
                'name': TestSingleLabelClassifierModel.get_name(),
                'pk': 9999
            }))
        self.assertEqual(response.status_code, 404)

    def test_labelling_classifier_model(self):
        """Dispatch to a classifier labelling view"""
        document = Document.objects.create()
        response = self.client.get(
            reverse('django_learnit:document-labelling', kwargs={
                'name': TestSingleLabelClassifierModel.get_name(),
                'pk': document.pk
            }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['view'].__class__, ClassifierModelLabellingView)
