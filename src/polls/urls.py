from django.urls import path

from .views import *

app_name = 'polls'

urlpatterns = [
    path('', PollsIndexView.as_view(), name='index'),
    path('<int:pk>/', PollsDetailView.as_view(), name='detail'),
    path('<int:question_id>/vote', vote, name='vote'),
    path(
        '<int:pk>/results',
        PollsDetailView.as_view(template_name='polls/pages/results.html'),
        name='results'
    ),
    path(
        'api/charts/result/<int:poll_id>',
        ChartResultView.as_view(),
        name="api_results_chart"
    ),
]
