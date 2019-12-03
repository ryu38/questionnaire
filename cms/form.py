from django import forms
from cms.models import Question, Choice


class QuestionForm(forms.ModelForm):

    READONLY_FIELDS = ('date_created', )

    def __init__(self, readonly_form=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        if readonly_form:
            for field in self.READONLY_FIELDS:
                self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Question
        fields = ('text', 'date_created', )


ChoiceFormset = forms.inlineformset_factory(
    Question, Choice, fields=('choice',),
    extra=2, max_num=4
)
