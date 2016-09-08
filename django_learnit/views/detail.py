from django.views.generic import TemplateView

from .base import LearningModelMixin


class LearningModelDetailView(LearningModelMixin, TemplateView):
    """
    LearningModel detail view
    """

    def get(self, *args, **kwargs):
        self.learning_model = self.get_learning_model()
        return super(LearningModelDetailView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds learning model context data
        """
        context = super(LearningModelDetailView, self).get_context_data(**kwargs)

        # Add the 10 most recently edited LabelledDocuments
        context['recently_updated_labelled_documents'] = self.learning_model\
            .get_labelled_documents_queryset()\
            .order_by('-modified')[:10]

        return context

    def get_template_names(self):
        """
        Returns learning model specific template name along with a default one
        to easily allow template overriding
        """
        return [
            'django_learnit/learning_models/%(name)s_detail.html' % {
                'name': self.learning_model.get_name()
            },
            'django_learnit/learning_models/detail.html'
        ]
