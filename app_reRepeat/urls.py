from django.urls import path

from . import views

app_name = 'app_reRepeat'

urlpatterns = [
        path('', views.index, name="home"),
        path('answer/', views.answer_questions, name="answer"),
        path('add/', views.add_questions, name="add"),
        path('edit/', views.edit_questions, name="edit"),
        path('<int:question_id>/', views.show_question, name="question"),
        path('add/add_confirm/', views.add_confirm, name="add_confirm"),
]
