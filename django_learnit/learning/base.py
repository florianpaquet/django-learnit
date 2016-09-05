from ..exceptions import ImproperlyConfigured


class LearningModelBuilderMixin(object):
    """
    Adds top level model building methods.

    Feature extraction, model definition and all machine learning related stuff
    is up to the developer. We don't assume anything here, leaving it extendable.
    """

    def __init__(self):
        """
        Initialize the learning model
        """
        super(LearningModelBuilderMixin, self).__init__()
        self.model = self.load_model()

    def get_labelled_documents_queryset(self):
        """
        Returns LabelledDocument queryset for the learning model
        """
        from django.contrib.contenttypes.models import ContentType
        from ..models import LabelledDocument

        return LabelledDocument.objects\
            .filter(model_name=self.get_name())

    def load_model(self):
        """
        Loads the model and returns it
        """
        pass

    def save_model(self):
        """
        Saves the model
        """
        pass

    def build_model(self, labelled_documents):
        """
        Build the model
        """
        raise NotImplementedError()

    def build(self):
        """
        Builds and saves the model
        """
        labelled_documents = self.get_labelled_documents_queryset()

        self.model = self.build_model(labelled_documents)
        self.save_model()


class LearningModel(LearningModelBuilderMixin):
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

    def get_unlabelled_documents_queryset(self):
        """
        Returns the unlabelled documents queryset
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

        return queryset.exclude(pk__in=labelled_ids)

    def get_random_unlabelled_document(self):
        """
        Returns a random unlabelled document
        """
        # Return a random unlabelled document or None
        try:
            return self.get_unlabelled_documents_queryset()\
                .order_by('?')[0]
        except IndexError:
            return None

    def is_classifier(self):
        """
        Returns whether the model inherits from a classifier model or not
        """
        from .classifier import ClassifierModel
        return issubclass(self.__class__, ClassifierModel)

    def predict(self, documents):
        """
        Predict output for documents
        """
        raise NotImplementedError()
