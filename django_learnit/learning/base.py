from ..exceptions import ImproperlyConfigured


class LearningModel(object):
    """
    Base learning model identified by a name
    and holding a document queryset
    """
    name = None
    queryset = None

    @classmethod
    def get_name(cls):
        """
        Returns the learning model name
        Raises `ImproperlyConfigured` when not set
        """
        # No `name` set
        if not cls.name:
            raise ImproperlyConfigured("%(cls)s is missing a name." % {
                'cls': cls.__name__
            })

        # `name` is not a non empty string
        if not isinstance(cls.name, str) or not cls.name.strip():
            raise ImproperlyConfigured("%(cls)%s name must be a non empty string." % {
                'cls': cls.__name__
            })

        return cls.name

    def get_queryset(self):
        """
        Returns the documents queryset
        Raises `ImproperlyConfigured` when not set
        """
        if self.queryset is None:
            raise ImproperlyConfigured("%(cls)s is missing a QuerySet." % {
                'cls': self.__class__.__name__
            })

        return self.queryset.all()

    def get_random_unlabelled_document(self):
        """
        Returns a random unlabelled document
        """
        from django.contrib.contenttypes.models import ContentType
        from ..models import LabelledDocument

        queryset = self.get_queryset()

        # Retrieve labelled IDs
        labelled_ids = LabelledDocument.objects\
            .filter(
                document_content_type=ContentType.objects.get_for_model(queryset.model),
                model_name=self.get_name())\
            .values_list('document_id', flat=True)

        # Return a random unlabelled document or None
        try:
            return queryset\
                .exclude(pk__in=labelled_ids)\
                .order_by('?')[0]
        except IndexError:
            return None

    def is_classifier(self):
        """
        Returns whether the model inherits from a classifier model or not
        """
        from .classifier import ClassifierModel
        return issubclass(self.__class__, ClassifierModel)
