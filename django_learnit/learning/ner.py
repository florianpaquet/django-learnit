from .base import LearningModel
from .classifier import ClassifierMixin


class NamedEntityRecognizerModel(ClassifierMixin, LearningModel):
    """
    TODO : Create a ClassificationMixin for stuff related to classes (NER shares
    classes with ClassifierModel)
    """

    def get_tokens(self, document):
        """
        Outputs tokens for the document.

        The numbers of tokens must be exactly the same for labelling task and
        model training task.

        Here, you usually return the output of the model tokenizer.
        """
        raise NotImplementedError()
