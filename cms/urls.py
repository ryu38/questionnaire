from django.urls import path
from cms import views

app_name = 'cms'
urlpatterns = [
    path('', views.QuestionList.as_view(), name='question_list'),
    path('add', views.add_question, name='add'),
    path('form', views.create, name='form'),
    path('yours', views.UsersQuestionList.as_view(), name='your_question_list'),
    path('question/<int:pk>/like/', views.like, name='like'),
    path('vote', views.vote, name='vote'),
    path('test', views.test, name='test'),
    path('question/create', views.create_question, name='create'),
    path('favorite', views.LikedList.as_view(), name='favorite_list'),
]
