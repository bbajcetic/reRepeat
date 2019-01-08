from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Question

##first way: fill context, load template, return Http object with the result of rendered template
#def index(request):
#    question_list = Question.objects.all()
#    context = {
#            'question_list':question_list,
#    }
#    template = loader.get_template('app_reRepeat/index.html')
#    return HttpResponse(template.render(context))

##second way: (no longer need to import loader and HttpResponse) render function takes the request object, template, and dictionary/context as arguments and returns HttpResponse object of the given template rendered with the given context
def index(request):
    return render(request, 'app_reRepeat/index.html')

def answer_questions(request):
    question_list = Question.objects.all()
    context = {'question_list':question_list,}
    return render(request, 'app_reRepeat/answer.html', context)

def add_questions(request):
    question_list = Question.objects.all()
    context = {'question_list':question_list,}
    return render(request, 'app_reRepeat/add.html', context)

def edit_questions(request):
    question_list = Question.objects.all()
    context = {'question_list':question_list,}
    return render(request, 'app_reRepeat/edit.html', context)

def show_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question,}
    return render(request, 'app_reRepeat/show_question.html', context)
