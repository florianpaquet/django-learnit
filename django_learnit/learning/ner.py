from .base import LearningModel
from .classifier import GenericClassifierMixin

from ..exceptions import ImproperlyConfigured


class NamedEntityRecognizerModel(GenericClassifierMixin, LearningModel):
    """
    NER model that associates a label to each token
    """
    default_class = None

    def get_default_class(self):
        """
        Returns the default class.
        Raise `ImproperlyConfigured` if it's not an available class
        """
        if self.default_class is None:
            raise ImproperlyConfigured("%(name)s is missing a default class." % {
                'name': self.__class__.__name__
            })

        if self.default_class not in dict(self.get_classes()):
            raise ImproperlyConfigured("%(name)s is not an available class." % {
                'name': self.default_class
            })

        return self.default_class

    def get_tokens(self, document):
        """
        Outputs tokens for the document.

        The numbers of tokens must be exactly the same for labelling task and
        model training task.

        Here, you usually return the output of the model tokenizer.
        """
        raise NotImplementedError()
