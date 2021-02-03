from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('There is no qusestion with id %s on data base!' % question_id)
    context = {
        'question': question
    }
    return render(request, 'polls/detail.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = { 'question': question }
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    response = "You're seeing results for question %s."
    return HttpResponse(response % question_id)
