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

    def is_classifier(self):
        """
        Returns whether the model inherits from a classifier model or not
        """
        from .classifier import ClassifierModel
        return issubclass(self.__class__, ClassifierModel)
