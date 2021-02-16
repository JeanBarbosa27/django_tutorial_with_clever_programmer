from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from polls.models import Question, Choice

class PollsIndexView(ListView):
    template_name = 'polls/pages/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class PollsDetailView(DetailView):
    model = Question
    template_name = 'polls/pages/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())



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

        return render(request, 'polls/pages/detail.html', context)

class ChartResultView(APIView):

    def get(self, request, *args, **kwargs):
        choices = Question.objects.get(id=kwargs['poll_id']).choice_set.all()
        labels = [choice.choice_text for choice in choices]
        votes = [choice.votes for choice in choices]

        data = {
            'labels': labels,
            'votes': votes,
        }

        return Response(data)
