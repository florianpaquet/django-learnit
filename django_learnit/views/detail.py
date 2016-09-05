from django.views.generic import TemplateView

from .base import LearningModelMixin


class LearningModelDetailView(LearningModelMixin, TemplateView):
    """
    LearningModel detail view
    """

    def get(self, *args, **kwargs):
        self.learning_model = self.get_learning_model()
        return super(LearningModelDetailView, self).get(*args, **kwargs)

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
