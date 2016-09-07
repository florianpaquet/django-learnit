from functools import (
    partial,
    wraps)
from django.forms import formset_factory

from ..forms.ner import NamedEntityRecognizerForm

from .base import BaseLearningModelLabellingView
from .classifier import GenericClassifierModelLabellingMixin


class NamedEntityRecognizerModelLabellingMixin(GenericClassifierModelLabellingMixin):
    """
    Mixin for a NER model document labelling
    """

    def get_context_data(self, **kwargs):
        """
        Adds document tokens in the context
        """
        context = super(NamedEntityRecognizerModelLabellingMixin, self)\
            .get_context_data(**kwargs)
        context['tokens'] = self.tokens
        context['classes_colors'] = self.learning_model.get_classes_with_colors()

        return context

    def get_form_class(self):
        """
        Returns the `NamedEntityRecognizerForm` formset
        """
        n_tokens = len(self.tokens)

        return formset_factory(
            wraps(NamedEntityRecognizerForm)(partial(NamedEntityRecognizerForm, classes=self.get_classes())),
            min_num=n_tokens,
            max_num=n_tokens,
            extra=0)

    def get_initial(self):
        """
        Builds a default initial data with outside_class if initial data length
        differs from tokens length.
        """
        initial = super(NamedEntityRecognizerModelLabellingMixin, self).get_initial()

        if len(initial) != len(self.tokens):
            initial = [{'label': self.learning_model.outside_class}] * len(self.tokens)

        return initial


class NamedEntityRecognizerModelLabellingView(NamedEntityRecognizerModelLabellingMixin,
                                              BaseLearningModelLabellingView):
    template_name = 'django_learnit/labelling/ner.html'

    def get(self, *args, **kwargs):
        self.learning_model = self.get_learning_model()
        self.object = self.get_object()
        self.tokens = self.learning_model.get_tokens(self.object)
        return super(BaseLearningModelLabellingView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.learning_model = self.get_learning_model()
        self.object = self.get_object()
        self.tokens = self.learning_model.get_tokens(self.object)
        return super(BaseLearningModelLabellingView, self).post(*args, **kwargs)
