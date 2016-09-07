from .base import LearningModel
from .classifier import GenericClassifierMixin


class NamedEntityRecognizerModel(GenericClassifierMixin, LearningModel):
    """
    NER model that associates a label to each token
    """
    outside_class = 'O'
    outside_class_display = 'Outside'
    outside_color = '#CCCCCC'

    default_colors = [
        '#AB47BC',
        '#F44336',
        '#303F9F',
        '#448AFF',
        '#00796B',
        '#8BC34A',
        '#FBC02D',
        '#4E342E'
    ]

    def get_classes(self):
        """
        Returns classes with preprended oustide class
        """
        out_classes = ()
        classes = super(NamedEntityRecognizerModel, self).get_classes()

        for c in classes:
            out_classes += (c[:2],)

        return ((self.outside_class, self.outside_class_display),) + out_classes

    def get_tokens(self, document):
        """
        Outputs tokens for the document.

        The numbers of tokens must be exactly the same for labelling task and
        model training task.

        Here, you usually return the output of the model tokenizer.
        """
        raise NotImplementedError()

    def get_classes_with_colors(self):
        """
        Returns classes with their associated colors
        If there's no explicit color, pick one in the `default_colors` list
        """
        i = 0
        out_classes = ()
        classes = super(NamedEntityRecognizerModel, self).get_classes()

        for c in classes:
            if len(c) != 3:
                c += (self.default_colors[i],)
                i += 1
            out_classes += (c,)

        return (
            (self.outside_class, self.outside_class_display, self.outside_color),
        ) + out_classes
