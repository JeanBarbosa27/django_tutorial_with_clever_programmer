from django.urls import path

from .views import *

app_name = 'polls'

urlpatterns = [
    path('', PollsIndexView.as_view(), name='index'),
    path('<int:pk>/', PollsDetailView.as_view(), name='detail'),
    path('<int:question_id>/vote', vote, name='vote'),
    path(
        '<int:pk>/results',
        PollsDetailView.as_view(template_name='polls/results.html'),
        name='results'
    ),
]
