from django.views.generic.detail import SingleObjectMixin

from ..library import get_learning_model


class LearningModelMixin(object):
    """
    Mixin for LearningModel base
    """

    def get_learning_model(self):
        """
        Returns the learning model corresponding to the name
        in the URL pattern.

        Model existence is checked on the dispatch view
        `labelleling_view_dispatch` so we don't need to check here again.
        """
        model_name = self.kwargs['name']
        return get_learning_model(model_name)

    def get_context_data(self, **kwargs):
        """
        Adds the document detail template name for the learning model
        """
        context = super(LearningModelMixin, self).get_context_data(**kwargs)
        context['document_detail_template_name'] = 'learning_models/%(name)s.html' % {
            'name': self.learning_model.get_name()
        }

        return context


class DocumentMixin(SingleObjectMixin):
    """
    Learning model related document mixin
    """
    context_object_name = 'document'

    def get_queryset(self):
        """
        Returns the learning model queryset
        """
        return self.learning_model.get_queryset()
