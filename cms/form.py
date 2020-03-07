from django import forms
from cms.models import Question, Choice
from django.contrib.auth.forms import AuthenticationForm


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text', )
        # widgets = {
        #     'date_created': forms.DateTimeInput(attrs={'readonly': True})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


ChoiceFormset = forms.inlineformset_factory(
    Question, Choice, form=QuestionForm, fields=('choice',),
    extra=2, can_delete=False, max_num=4
)


# class LoginForm(AuthenticationForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['placeholder'] = field.label
