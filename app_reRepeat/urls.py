from django.urls import path

from . import views

app_name = 'app_reRepeat'

urlpatterns = [
        path('', views.index, name="home"),
        path('answer/', views.answer_questions, name="answer"),
        path('answer/setup/', views.answer_setup, name="answer_setup"),
        path('answer_from_edit/<int:question_id>/<int:show_answer>/', views.answer_from_edit, name="answer_from_edit"),
        path('answer/<int:show_answer>/', views.answer_question, name="answer_question"),
        path('answer/process_answer/<int:question_id>/', views.process_answer, name="process_answer"),
        path('answer/process_answer_from_edit/<int:question_id>/', views.process_answer_from_edit, name="process_answer_from_edit"),
        path('add/', views.add_questions, name="add"),
        path('edit/', views.edit_questions, name="edit"),
        path('show/<int:question_id>/', views.show_question, name="show_question"),
        path('edit/<int:question_id>/', views.edit_question, name="edit_question"),
        path('add/add_confirm/', views.add_confirm, name="add_confirm"),
        path('edit/<int:question_id>/update_confirm/', views.update_confirm, name="update_confirm"),
        path('edit/<int:question_id>/delete_confirm/', views.delete_confirm, name="delete_confirm"),
        path('delete/<int:question_id>/', views.delete_question, name="delete_question"),
]
