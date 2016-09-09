from ..exceptions import ImproperlyConfigured

from .base import LearningModel


class GenericClassifierMixin(object):
    """
    Classifier mixin holding available classes for the learning model
    """
    classes = ()
    default_classes_colors = (
        '#AB47BC',
        '#F44336',
        '#303F9F',
        '#448AFF',
        '#00796B',
        '#8BC34A',
        '#FBC02D',
        '#4E342E'
    )

    def get_classes(self):
        """
        Returns the classifier output classes.
        Implicitly transforms the key to a string.
        """
        if not self.classes:
            raise ImproperlyConfigured("%(cls)s is missing labels." % {
                'cls': self.__class__.__name__
            })

        return tuple((str(c[0]), c[1]) for c in self.classes)

    def get_classes_with_colors(self):
        """
        Returns classes with their associated colors
        If there's no explicit color, pick one in the `default_classes_colors`
        """
        i = 0
        out_classes = ()

        for c in self.get_classes():
            if len(c) != 3:
                c += (self.default_classes_colors[i],)
                i += 1
            out_classes += (c,)

        return out_classes


class ClassifierModel(GenericClassifierMixin, LearningModel):
    """
    Base classifier learning model that outputs one or
    more labels for each document
    """
    multilabel = False
