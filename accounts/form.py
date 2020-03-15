from django import forms
from accounts.models import UserInformation, UserImage


class UserInformationForm(forms.ModelForm):

    class Meta:
        model = UserInformation
        fields = ('nickname', 'age')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'
        self.fields['age'].required = False
        self.fields['age'].widget.attrs['max'] = 100
        self.fields['age'].widget.attrs['min'] = 15


class UserImageForm(forms.ModelForm):

    class Meta:
        model = UserImage
        fields = ('image',)
