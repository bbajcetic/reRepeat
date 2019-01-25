from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from .models import Question, QuestionForm
import re

TAG_LIST = []

def SignupView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('app_reRepeat:home'))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'User created!')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserCreationForm()

    return render(request, 'app_reRepeat/signup.html', {'form':form})

class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app_reRepeat/index.html'

@login_required
def AnswerView(request):
    global TAG_LIST
    if request.method == 'POST':
        reset_skipped()
        tags = request.POST.get('tags', False)
        if not tag_check(tags):
            messages.add_message(request, messages.INFO, 'Invalid tag given (no symbols allowed)')
            return render(request, 'app_reRepeat/answer.html')
        TAG_LIST = get_tag_list(tags) if tags else []
        return HttpResponseRedirect(reverse('app_reRepeat:answer_question', args=(0,)))

    return render(request, 'app_reRepeat/answer.html')

class DisplayView(LoginRequiredMixin, generic.list.ListView):
    model = Question
    template_name = 'app_reRepeat/edit.html'
    context_object_name = 'question_list'

class ShowQuestionView(LoginRequiredMixin, generic.detail.DetailView):
    model = Question
    template_name = 'app_reRepeat/show_question.html'

@login_required
def AddQuestionView(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q_text = form.cleaned_data['question_text']
            a_text = form.cleaned_data['answer_text']
            tags = form.cleaned_data['tags']
            if not tag_check(tags):
                messages.add_message(request, messages.INFO, 'Invalid tag given')
                return render(request, 'app_reRepeat/add.html', {'form':form})
            new_question = Question(question_text=q_text,answer_text=a_text,tags=tags,update_date=timezone.now())
            new_question.save()
            new_id = new_question.pk
            messages.add_message(request, messages.INFO, 'Question created!')
            return HttpResponseRedirect(reverse('app_reRepeat:show_question', args=(new_id,)))
    else:
        form = QuestionForm()

    return render(request, 'app_reRepeat/add.html', {'form':form})

@login_required
def EditQuestionView(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        if request.POST.get('delete', False):
            return HttpResponseRedirect(reverse('app_reRepeat:delete_question', args=(question_id,)))
        form = QuestionForm(request.POST)
        if form.is_valid():
            q_text = form.cleaned_data['question_text']
            a_text = form.cleaned_data['answer_text']
            tags = form.cleaned_data['tags']
            if not tag_check(tags):
                messages.add_message(request, messages.INFO, 'Invalid tag given')
                return render(request, 'app_reRepeat/edit_question.html', {'form':form, 'question':question})
            question.question_text = q_text
            question.answer_text = a_text
            question.tags=tags
            question.save()
            messages.add_message(request, messages.INFO, 'Question updated')
            return HttpResponseRedirect(reverse('app_reRepeat:show_question', args=(question_id,)))
    else:
        form = QuestionForm(instance=question)

    return render(request, 'app_reRepeat/edit_question.html', {'form':form, 'question':question})

@login_required
def DeleteQuestionView(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        if request.POST.get('delete', False):
            question.delete()
            messages.add_message(request, messages.INFO, 'Question deleted!')
            return HttpResponseRedirect(reverse('app_reRepeat:edit'))
        elif request.POST.get('not_delete', False):
            messages.add_message(request, messages.INFO, 'Question not deleted')
            return HttpResponseRedirect(reverse('app_reRepeat:edit_question', args=(question_id,)))

    return render(request, 'app_reRepeat/delete_question.html', {'question':question})

@login_required
def process_answer_from_edit(request, question_id): #redirect
    question = get_object_or_404(Question, pk=question_id)
    if request.POST.get('next', False) and ( question.is_ready() or question.is_soon() ):
        question.update_counter()
        question.save()
        messages.add_message(request, messages.INFO, 'Question reviewed!')
    return HttpResponseRedirect(reverse('app_reRepeat:edit'))
    
@login_required
def process_answer(request, question_id): #redirect
    question = get_object_or_404(Question, pk=question_id)
    if request.POST.get('skip', False):
        question.skip = True
        question.save()
    elif request.POST.get('next', False):
        #process the answer and update the question counter, etc:
        question.update_counter()
        question.save()
    return HttpResponseRedirect(reverse('app_reRepeat:answer_question', args=(0,)))

@login_required
def answer_from_edit(request, question_id, show_answer):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question, 'show_answer':show_answer,}
    return render(request, 'app_reRepeat/answer_from_edit.html', context)

@login_required
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

def get_tag_list(tag_string):
    tag_list = tag_string.lower().split(',')
    tag_list = list(tag.replace(' ','') for tag in tag_list)
    tag_list = list(filter(None, tag_list))
    return tag_list

def tag_check(tags):
    tag_pattern = re.compile("[^ ,a-zA-Z0-9]")
    if tag_pattern.search(tags):
        return False #found invalid characters for Question.tag
    return True

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

