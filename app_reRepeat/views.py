from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
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
    return render(request, 'app_reRepeat/answer.html')

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

def add_confirm(request):
    q_text = request.POST['question_text']
    a_text = request.POST['answer_text']
    new_question = Question(question_text=q_text,answer_text=a_text,update_date=timezone.now())
    new_question.save()
    new_id = new_question.pk

    return HttpResponseRedirect(reverse('app_reRepeat:show_question', args=(new_id,)))

def update_confirm(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.question_text=request.POST['question_text']
    question.answer_text=request.POST['answer_text']
    question.save()

    return HttpResponseRedirect(reverse('app_reRepeat:show_question', args=(question_id,)))

def delete_confirm(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question,}
    return render(request, 'app_reRepeat/delete_confirm.html', context)

def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question,}
    return render(request, 'app_reRepeat/edit_question.html', context)

def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.POST.get('delete', False):
        question.delete()
        return HttpResponseRedirect(reverse('app_reRepeat:edit'))
    elif request.POST.get('not_delete', False):
        return HttpResponseRedirect(reverse('app_reRepeat:edit_question', args=(question_id,)))

def answer_setup(request):
    #get setup info (tags to answer, etc.)
    return HttpResponseRedirect(reverse('app_reRepeat:home'))

def answer_question(request):
    return HttpResponseRedirect(reverse('app_reRepeat:home'))
