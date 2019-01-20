from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .models import Question
import re

TAG_LIST = []

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
    if not q_text or not a_text:
        messages.add_message(request, messages.INFO, 'Question and answer fields must be filled')
        return HttpResponseRedirect(reverse('app_reRepeat:add'))

    tags = request.POST['tags']
    if not tag_check(tags):
        tags = ""
    new_question = Question(question_text=q_text,answer_text=a_text,tags=tags,update_date=timezone.now())
    new_question.save()
    new_id = new_question.pk
    messages.add_message(request, messages.INFO, 'Question created!')

    return HttpResponseRedirect(reverse('app_reRepeat:show_question', args=(new_id,)))

def update_confirm(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    q_text = request.POST['question_text']
    a_text = request.POST['answer_text']
    if not q_text or not a_text:
        messages.add_message(request, messages.INFO, 'Question and answer fields must be filled')
        return HttpResponseRedirect(reverse('app_reRepeat:edit_question', args=(question_id,)))
    question.question_text = q_text
    question.answer_text = a_text
    tags = request.POST['tags']
    if tag_check(tags):
        question.tags=tags
    else:
        messages.add_message(request, messages.INFO, 'Invalid tag given (no symbols allowed)')
        return HttpResponseRedirect(reverse('app_reRepeat:edit_question', args=(question_id,)))

    question.save()
    messages.add_message(request, messages.INFO, 'Question updated')

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
        messages.add_message(request, messages.INFO, 'Question deleted!')
        return HttpResponseRedirect(reverse('app_reRepeat:edit'))
    elif request.POST.get('not_delete', False):
        messages.add_message(request, messages.INFO, 'Question not deleted')
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

def tag_check(tags):
    tag_pattern = re.compile("[^ ,a-zA-Z0-9]")
    if tag_pattern.search(tags):
        return False #found invalid characters for Question.tag
    return True

def answer_setup(request):
    global TAG_LIST
    reset_skipped()
    tags = request.POST.get('tags', False)
    if not tag_check(tags):
        tags = ""
        messages.add_message(request, messages.INFO, 'Invalid tag given (no symbols allowed)')
    TAG_LIST = get_tag_list(tags) if tags else []
    #get setup info (tags to answer, etc.)
    #for actual setup, there will be an html page for this where you have to click continue and then it redirects to answer_question
    #^for now though, just redirect to answer_question
    return HttpResponseRedirect(reverse('app_reRepeat:answer_question', args=(0,)))

def process_answer_from_edit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.POST.get('next', False) and ( question.is_ready() or question.is_soon() ):
        question.update_counter()
        question.save()
        messages.add_message(request, messages.INFO, 'Question reviewed!')
    return HttpResponseRedirect(reverse('app_reRepeat:edit'))
    
def process_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.POST.get('skip', False):
        question.skip = True
        question.save()
    elif request.POST.get('next', False):
        #process the answer and update the question counter, etc:
        question.update_counter()
        question.save()
    return HttpResponseRedirect(reverse('app_reRepeat:answer_question', args=(0,)))

def tags_match(tags):
    """
    Returns True if at least one of the tags in the tags string argument match one of the tags in TAG_LIST or if TAG_LIST is empty because that means no tags are specified. Returns False otherwise.
    """
    if not TAG_LIST:
        return True
    tags = get_tag_list(tags)
    for tag in TAG_LIST:
        if tag in tags:
            return True
    return False

def answer_from_edit(request, question_id, show_answer):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question, 'show_answer':show_answer,}
    return render(request, 'app_reRepeat/answer_from_edit.html', context)

def answer_question(request, show_answer):
    question_list = Question.objects.all()
    if not question_list.exists():
        return HttpResponseRedirect(reverse('app_reRepeat:answer'))
        messages.add_message(request, messages.INFO, 'No questions exist yet!')
    next_question = -1
    for q in question_list:
        if q.is_ready() and not q.is_skipped() and tags_match(q.tags):
            if next_question == -1:
                next_question = q
            elif q.review_percent() > next_question.review_percent():
                next_question = q
    context = {'question':next_question, 'show_answer':show_answer,}
    if next_question == -1:
        if reset_skipped() == True:
            return HttpResponseRedirect(reverse('app_reRepeat:answer_question', args=(0,)))
        else:
            messages.add_message(request, messages.INFO, 'No questions are ready for review')
            return HttpResponseRedirect(reverse('app_reRepeat:answer'))
    else:
        return render(request, 'app_reRepeat/answer_question.html', context)

