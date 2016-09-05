from django.apps import apps
from django.views.generic import TemplateView


class LearningModelListView(TemplateView):
    """
    Lists registered learning models in the application
    """
    template_name = 'django_learnit/learning_models/list.html'

    def get_context_data(self, **kwargs):
        """
        Adds registered learning models in the context
        """
        context = super(LearningModelListView, self).get_context_data(**kwargs)

        app_config = apps.get_app_config('django_learnit')
        context['learning_models'] = app_config.learning_models

        return context
