from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LabelledDocumentManager(models.Manager):

    def get_for_document(self, document, model_name):
        """
        Returns the LabelledDocument instance for the document instance
        and the model name. Returns None if not found.
        """
        try:
            return self.get_queryset().get(
                document_content_type=ContentType.objects.get_for_model(document),
                document_id=document.pk,
                model_name=model_name)
        except self.model.DoesNotExist:
            return None

    def update_or_create_for_document(self, document, model_name, value):
        """
        Updates or creates the LabelledDocument instance for the given
        document and model name with the value.
        """
        return self.update_or_create(
            document_content_type=ContentType.objects.get_for_model(document),
            document_id=document.pk,
            model_name=model_name,
            defaults={
                'value': value
            })


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

    value = models.TextField()

    objects = LabelledDocumentManager()

    class Meta:
        unique_together = ('model_name', 'document_content_type', 'document_id')
