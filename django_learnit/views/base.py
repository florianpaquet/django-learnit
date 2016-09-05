from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.views.generic import (
    FormView,
    RedirectView)
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
        """
        model_name = self.kwargs['name']
        learning_model = get_learning_model(model_name)

        if not learning_model:
            raise Http404("Learning model `%(name)s` is not registered" % {
                'name': model_name
            })

        return learning_model

    def get_context_data(self, **kwargs):
        """
        Adds LearningModel data in the context
        """
        context = super(LearningModelMixin, self).get_context_data(**kwargs)

        context['learning_model'] = self.learning_model
        context['learning_model_name'] = self.learning_model.get_name()

        return context

    def get_random_unlabelled_document_url(self):
        """
        Returns a random unlabelled document url for the learning model
        """
        document = self.learning_model.get_random_unlabelled_document()

        if document:
            url = reverse('django_learnit:document-labelling', kwargs={
                'name': self.learning_model.get_name(),
                'pk': document.pk
            })
        else:
            # Maybe : add a message using django.contrib.messages
            url = reverse('django_learnit:learning-model-detail', kwargs={
                'name': self.learning_model.get_name()
            })

        return url


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
    """
    LabelledDocument form mixin providing initial data &
    post success action.
    """

    def get_context_data(self, **kwargs):
        """
        Adds the document detail template name for the learning model
        """
        context = super(LabelledDocumentFormMixin, self).get_context_data(**kwargs)
        context['document_detail_template_name'] = 'django_learnit/document_labelling/%(name)s_detail.html' % {
            'name': self.learning_model.get_name()
        }

        return context

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

        return super(LabelledDocumentFormMixin, self).form_valid(form)


class BaseLearningModelLabellingView(LearningModelMixin, DocumentMixin,
                                     LabelledDocumentFormMixin, FormView):

    def get(self, *args, **kwargs):
        self.learning_model = self.get_learning_model()
        self.object = self.get_object()
        return super(BaseLearningModelLabellingView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.learning_model = self.get_learning_model()
        self.object = self.get_object()
        return super(BaseLearningModelLabellingView, self).post(*args, **kwargs)

    def get_success_url(self):
        return self.get_random_unlabelled_document_url()


class RandomUnlabelledDocumentRedirectView(LearningModelMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        self.learning_model = self.get_learning_model()
        return self.get_random_unlabelled_document_url()
