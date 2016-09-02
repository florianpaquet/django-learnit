from django.test import TestCase
from django.core.urlresolvers import reverse


class LearningModelURLRoutingTestCase(TestCase):

    def test_labelling_non_registered_model(self):
        """HTTP 404 when model is not registered"""
        response = self.client.get(
            reverse('django_learnit:document-labelling', kwargs={
                'name': 'missingmodel',
                'pk': 1
            }))
        self.assertEqual(response.status_code, 404)
