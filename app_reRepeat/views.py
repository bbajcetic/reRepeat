from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from .models import Question
import re

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

def get_tag_list(tag_string):
    tag_list = tag_string.lower().split(',')
    tag_list = list(tag.replace(' ','') for tag in tag_list)
    tag_list = list(filter(None, tag_list))
    return tag_list

def add_confirm(request):
    q_text = request.POST['question_text']
    a_text = request.POST['answer_text']
    tags = request.POST['tags']
    tag_pattern = re.compile("[^ ,a-zA-Z0-9]")
    if tag_pattern.search(tags):
        tags = ""
    new_question = Question(question_text=q_text,answer_text=a_text,tags=tags,update_date=timezone.now())
    new_question.save()
    new_id = new_question.pk

    return HttpResponseRedirect(reverse('app_reRepeat:show_question', args=(new_id,)))

def update_confirm(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.question_text=request.POST['question_text']
    question.answer_text=request.POST['answer_text']
    tags = request.POST['tags']
    tag_pattern = re.compile("[^ ,a-zA-Z0-9]")
    if not tag_pattern.search(tags):
        question.tags=tags

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

def reset_skipped():
    skipped = False
    #reset all skipped questions to unskipped
    question_list = Question.objects.all()
    for q in question_list:
        if q.skip == True:
            q.skip = False
            q.save()
            skipped = True
    return skipped

def answer_setup(request):
    reset_skipped()
    #get setup info (tags to answer, etc.)
    #for actual setup, there will be an html page for this where you have to click continue and then it redirects to answer_question
    #^for now though, just redirect to answer_question
    return HttpResponseRedirect(reverse('app_reRepeat:answer_question', args=(0,)))

def process_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.POST['skip']:
        question.skip = True
        question.save()
    elif request.POST['next']:
        #process the answer and update the question counter, etc:
        question.update_counter()
        question.save()
    return HttpResponseRedirect(reverse('app_reRepeat:answer_question', args=(0,)))

def answer_question(request, show_answer):
    question_list = Question.objects.all()
    if not question_list.exists():
        return HttpResponseRedirect(reverse('app_reRepeat:answer'))
        #let the user know there are no questions
    next_question = -1
    for q in question_list:
        if q.is_ready() and not q.is_skipped():
            if next_question == -1:
                next_question = q
            elif q.review_percent() > next_question.review_percent():
                next_question = q
    context = {'question':next_question, 'show_answer':show_answer,}
    if next_question == -1:
        if reset_skipped() == True:
            return HttpResponseRedirect(reverse('app_reRepeat:answer_question', args=(0,)))
        else:
            #also return message for no questions to answer
            return HttpResponseRedirect(reverse('app_reRepeat:answer'))
    else:
        return render(request, 'app_reRepeat/answer_question.html', context)

