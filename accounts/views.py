from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts.models import UserInformation
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class Information(generic.TemplateView):
    template_name = 'accounts/account.html'

    def get_context_data(self, **kwargs):
        ctx = super(Information, self).get_context_data(**kwargs)
        if UserInformation.objects.filter(user=self.request.user).exists():
            ctx['information'] = UserInformation.objects.get(user=self.request.user)
        else:
            new_information = UserInformation()
            new_information.user = self.request.user
            new_information.age = '非公開'
            new_information.sex = '非公開'
            new_information.save()
            ctx['information'] = UserInformation.objects.get(user=self.request.user)
        return ctx
