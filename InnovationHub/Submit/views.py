from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def submission(request):
    return HttpResponse("Submission")

def submissionForm(request):
    return HttpResponse("SubmissionForm")

def success(request):
    return HttpResponse("Submission Success")

def fail(request):
    return HttpResponse("Submission Failed")
