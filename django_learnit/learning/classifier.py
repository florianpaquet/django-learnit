from ..exceptions import ImproperlyConfigured

from .base import LearningModel


class GenericClassifierMixin(object):
    """
    Classifier mixin holding available classes for the learning model
    """
    classes = ()

    def get_classes(self):
        """
        Returns the classifier output classes.
        Implicitly transforms the key to a string.
        """
        if not self.classes:
            raise ImproperlyConfigured("%(cls)s is missing labels." % {
                'cls': self.__class__.__name__
            })

        return tuple(((str(c[0]),) + c[1:]) for c in self.classes)


class ClassifierModel(GenericClassifierMixin, LearningModel):
    """
    Base classifier learning model that outputs one or
    more labels for each document
    """
    multilabel = False
