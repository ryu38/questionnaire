from django.urls import path
from cms import views

app_name = 'cms'
urlpatterns = [
    path('', views.QuestionList.as_view(), name='question_list'),
    path('question/<int:pk>/like/', views.like, name='like'),
    path('question/<int:question_pk>/vote/<int:choice_pk>', views.vote, name='vote'),
    path('test', views.test, name='test'),
    path('question/create', views.create_question, name='create')
]
