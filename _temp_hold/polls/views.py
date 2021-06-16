from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'polls/detail.html', context)

def vote(request, question_id):
    selected_choice = request.POST['choice']
    question = Question.objects.get(id=question_id)
    choice = question.choice_set.get(id=selected_choice)
    choice.votes += 1
    choice.save()
    return HttpResponseRedirect("results") #% question_id)

def results(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'polls/results.html', {'question': question})
