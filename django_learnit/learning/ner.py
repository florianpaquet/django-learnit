from .base import LearningModel
from .classifier import GenericClassifierMixin


class NamedEntityRecognizerModel(GenericClassifierMixin, LearningModel):
    """
    NER model that associates a label to each token
    """
    outside_class = 'O'
    outside_class_display = 'OUTSIDE'

    def get_classes(self):
        """
        Returns classes with preprended oustide class
        """
        classes = super(NamedEntityRecognizerModel, self).get_classes()
        return ((self.outside_class, self.outside_class_display),) + classes

    def get_tokens(self, document):
        """
        Outputs tokens for the document.

        The numbers of tokens must be exactly the same for labelling task and
        model training task.

        Here, you usually return the output of the model tokenizer.
        """
        raise NotImplementedError()
