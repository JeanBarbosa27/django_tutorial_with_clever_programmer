from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

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
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "You must selected a choice to vote on it!"
        }

        return render(request, 'polls/detail.html', context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = { 'question': question }

    return render(request, 'polls/results.html', context)
