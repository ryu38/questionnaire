from django.urls import path
from . import views
from questionnaire import settings
from django.conf.urls.static import static


# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'accounts'

urlpatterns = [
    # ex: /accounts/signup/
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('information/', views.information, name='account'),
    path('information/edit', views.edit_information, name='edit_information'),
    path('information/add', views.add_question, name='add'),
]
