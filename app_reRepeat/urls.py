from django.urls import path

from . import views

app_name = 'app_reRepeat'

urlpatterns = [
        path('', views.IndexView.as_view(), name="home"),
        path('signup/', views.SignupView, name="signup"),
        path('answer/', views.AnswerView, name="answer"),
        path('answer_from_edit/<int:pk>/<int:show_answer>/', views.answer_from_edit, name="answer_from_edit"),
        path('answer/<int:show_answer>/', views.answer_question, name="answer_question"),
        path('answer/process_answer/<int:pk>/', views.process_answer, name="process_answer"),
        path('answer/process_answer_from_edit/<int:pk>/', views.process_answer_from_edit, name="process_answer_from_edit"),
        path('add/', views.AddQuestionView, name="add"),
        path('edit/', views.DisplayView.as_view(), name="edit"),
        path('show/<int:pk>/', views.ShowQuestionView, name="show_question"),
        path('edit/<int:pk>/', views.EditQuestionView, name="edit_question"),
        path('delete/<int:pk>/', views.DeleteQuestionView, name="delete_question"),
]
