import factory

from ..models import LabelledDocument


class LabelledDocumentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = LabelledDocument
