from ..exceptions import ImproperlyConfigured

from .base import LearningModel


class ClassifierModel(LearningModel):
    """
    Base classifier learning model that outputs one or
    more labels for each document
    """
    classes = ()
    multilabel = False

    def get_classes(self):
        """
        Returns the classifier output classes
        """
        if not self.classes:
            raise ImproperlyConfigured("%(cls)s is missing labels." % {
                'cls': self.__class__.__name__
            })

        return self.classes
