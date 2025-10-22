from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F
from .models import *

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions_list"
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[0:5]

class DetailsView(generic.DetailView):
    template_name = "polls/details.html"
    model = Question

class ResultsView(generic.DetailView):
    template_name = "polls/results.html"
    model = Question

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', 
                    {
                          "question": question, 
                          "error_message": "You didn't select choice"
                    })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
