from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LabelledDocument(models.Model):
    """
    Generic labelled document related to any
    existing model instance in the application
    """
    model_name = models.TextField()

    # Generic relation
    document_content_type = models.ForeignKey(ContentType)
    document_id = models.PositiveIntegerField()

    document = GenericForeignKey('document_content_type', 'document_id')

    class Meta:
        unique_together = ('model_name', 'document_content_type', 'document_id')
