from django.views.generic.detail import SingleObjectMixin

from ..library import get_learning_model
from ..models import LabelledDocument


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


class LabelledDocumentFormMixin(object):

    def get_initial(self):
        """
        Returns the initial value for the document using
        its related LabelledDocument
        """
        initial = {}
        labelled_document = LabelledDocument.objects.get_for_document(
            self.object, self.learning_model.get_name())

        if labelled_document:
            initial.update(labelled_document.deserialize_value())

        return initial

    def form_valid(self, form):
        """
        Updates or creates the LabelledDocument instance with
        form data as the value.
        """
        LabelledDocument.objects.update_or_create_for_document(
            document=self.object,
            model_name=self.learning_model.get_name(),
            value=LabelledDocument.serialize_value(form.cleaned_data))

        return super().form_valid(form)
