from django.urls import path

from . import views

app_name = 'app_reRepeat'

urlpatterns = [
        path('', views.IndexView.as_view(), name="home"),
        path('answer/', views.AnswerQuestionView.as_view(), name="answer"),
        path('answer/setup/', views.answer_setup, name="answer_setup"),
        path('answer_from_edit/<int:question_id>/<int:show_answer>/', views.answer_from_edit, name="answer_from_edit"),
        path('answer/<int:show_answer>/', views.answer_question, name="answer_question"),
        path('answer/process_answer/<int:question_id>/', views.process_answer, name="process_answer"),
        path('answer/process_answer_from_edit/<int:question_id>/', views.process_answer_from_edit, name="process_answer_from_edit"),
        path('add/', views.AddQuestionView, name="add"),
        path('edit/', views.DisplayView.as_view(), name="edit"),
        path('show/<int:pk>/', views.ShowQuestionView.as_view(), name="show_question"),
        path('edit/<int:question_id>/', views.EditQuestionView, name="edit_question"),
        path('delete/<int:question_id>/', views.DeleteQuestionView, name="delete_question"),
]
