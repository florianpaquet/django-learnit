from django import forms


class ClassifierChoicesMixin(object):

    def __init__(self, classes, *args, **kwargs):
        super(ClassifierChoicesMixin, self).__init__(*args, **kwargs)
        self.fields['label'].choices = classes


class SingleLabelClassifierForm(forms.Form):
    label = forms.ChoiceField(widget=forms.RadioSelect())


class MultiLabelClassifierForm(forms.Form):
    label = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
