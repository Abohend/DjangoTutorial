from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import *

def index(request):
    latest_questions_list = Question.objects.order_by("-pub_date")[0:5]
    context = {"latest_questions_list": latest_questions_list}
    return render(request, "polls/index.html", context)

def details(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/details.html", {"question": question})

def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s" % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s" % question_id)
