from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from  .models import *

# Create your views here.

#HomePage Views
def HomePage(request):
    context = {'Quota' : '00:31:23'}
    context['FeaturedPrint'] = list(FeaturedPrint.objects.all())

    for i in range(0, len(context.get('FeaturedPrint'))):
        for j in range(0, len(context.get('FeaturedPrint')) - i - 1):
            if(context.get('FeaturedPrint')[j].votes < context.get('FeaturedPrint')[j + 1].votes):
                temp = context.get('FeaturedPrint')[j]
                context.get('FeaturedPrint')[j] = context.get('FeaturedPrint')[j + 1]
                context.get('FeaturedPrint')[j + 1] = temp

    for i in range(3, len(context.get('FeaturedPrint'))):
        context.get('FeaturedPrint').pop()
    return render(request, 'HomePage.html', context)


#Schedule Views
def Schedule(request):
    prints = Job.objects.all()
    context = {'Quota' : '00:31:23',
               'Jobs'  : prints,
              }
    #for i in range(0, len(prints)):
        #context["Job"    + str(i)] = prints[i].__str__()
        #context["Status" + str(i)] = prints[i].status
    return render(request, 'SchedulePage.html', context)


#Submit Views
def Submission(request):
    context = {'Quota' : '00:31:23'}
    return render(request, 'SubmitFile.html', context)

def Preview(request):
    return HttpResponse("Preview your model")

def SubmissionForm(request):
    return HttpResponse("Submission Form")

def Success(request):
    return HttpResponse("Submission Success")

def Fail(request):
    return HttpResponse("Submission Fail")

def PrintData(request, jobid):
    printData = Job.objects.filter(job_id=jobid)
    context = {'Quota'   : '00:31:23',
               'JobData' : printData}
    return render(request, 'PrintData.html', context)


#Account Views
def AccountData(request):
    context = {'Quota' : '00:31:23'}
    return render(request, 'AccountData.html', context)

def EditAccount(request):
    return HttpResponse("Account Editor")

def Login(request):
    return HttpResponse("Login to Account")

def layout(request):
    context = {'Quota' : '00:31:23'}
    return render(request, 'layout.html', context)


#The Carl Segment
def CarlPage(request):
    context = {'Quota' : '00:31:23'}
    return render(request, 'CarlSegment.html', context)


#Featured Prints
def Featured(request):
    context = {'Quota' : '00:31:23',
               'Jobs'  : list(FeaturedPrint.objects.all())}

    for i in range(0, len(context.get('Jobs'))):
        for j in range(0, len(context.get('Jobs')) - i - 1):
            if(context.get('Jobs')[j].votes < context.get('Jobs')[j + 1].votes):
                temp = context.get('Jobs')[j]
                context.get('Jobs')[j] = context.get('Jobs')[j + 1]
                context.get('Jobs')[j + 1] = temp

    return render(request, 'FeaturedPrints.html', context)


#Raw Data Views
def Data(request):
    context = {}
    return render(request, 'RawData.html', context)
