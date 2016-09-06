from django.http import Http404

from ..library import get_learning_model
from ..views.classifier import ClassifierModelLabellingView
from ..views.ner import NamedEntityRecognizerModelLabellingView


def labelleling_view_dispatch(request, name, pk):
    """
    Dispatches the request to the corresponding labelling view.
    If the model name is not a registered one, raises a HTTP 404.
    """
    learning_model = get_learning_model(name)

    if not learning_model:
        raise Http404("Learning model `%(name)s` is not registered" % {
            'name': name
        })

    if learning_model.is_classifier():
        return ClassifierModelLabellingView.as_view()(request, name=name, pk=pk)
    elif learning_model.is_named_entity_recognizer():
        return NamedEntityRecognizerModelLabellingView.as_view()(request, name=name, pk=pk)
