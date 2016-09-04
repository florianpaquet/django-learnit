from ..forms.classifier import (
    SingleLabelClassifierForm,
    MultiLabelClassifierForm)

from .base import BaseLearningModelLabellingView


class ClassifierModelLabellingMixin(object):
    """
    Mixin for a classifier model
    """

    def get_classes(self):
        """
        Returns the learning model classes
        """
        return self.learning_model.get_classes()

    def get_context_data(self, **kwargs):
        """
        Adds context data for classification
        """
        context = super(ClassifierModelLabellingMixin, self).get_context_data(**kwargs)

        context['classes'] = self.get_classes()
        context['multilabel'] = self.learning_model.multilabel

        return context

    def get_form_class(self):
        """
        Returns the form class depending on multilabel classification
        """
        if self.learning_model.multilabel:
            return MultiLabelClassifierForm
        else:
            return SingleLabelClassifierForm

    def get_form_kwargs(self):
        """
        Adds model classes to the form kwargs
        """
        kwargs = super(ClassifierModelLabellingMixin, self).get_form_kwargs()
        kwargs['classes'] = self.get_classes()

        return kwargs


class ClassifierModelLabellingView(ClassifierModelLabellingMixin,
                                   BaseLearningModelLabellingView):
    template_name = 'django_learnit/labelling/classifier.html'
