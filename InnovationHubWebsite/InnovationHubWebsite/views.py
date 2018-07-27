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

    context['TopPrints'] = list(User.objects.all())

    context['BestPrintMonth'] = list(Job.objects.filter(job_id = 20))
    context['BestPrintYear' ] = list(Job.objects.filter(job_id = 20))

    return render(request, 'HomePage.html', context)



#Schedule Views
def Schedule(request):
    inQueue  = list(Job.objects.filter(status = "in Queue"))
    printing = list(Job.objects.filter(status = "Printing"))

    prints = []

    for i in range(0, len(inQueue)):
        prints.append(inQueue[i])

    for i in range(0, len(printing)):
        prints.append(printing[i])

    printed  = list(Job.objects.filter(status = "Printed"))

    #Sorting the lists
    for i in range(0, len(prints)):
        for j in range(0, len(prints) - i - 1):
            if(prints[j].job_id > prints[j + 1].job_id):
                temp = prints[j]
                prints[j] = prints[j + 1]
                prints[j + 1] = temp

    for i in range(0, len(printed)):
        for j in range(0, len(printed) - i - 1):
            if(printed[j].job_id > printed[j + 1].job_id):
                temp = printed[j]
                printed[j] = printed[j + 1]
                printed[j + 1] = temp

    #Formatting dates correctly
    for i in range(0, len(prints)):
        day  = prints[i].print_end_time.day
        month = prints[i].print_end_time.month
        year  = prints[i].print_end_time.year

        date = str(day) + ' / ' + str(month) + ' / ' + str(year)
        prints[i].endDate = date

    for i in range(0, len(printed)):
        day  = printed[i].print_end_time.day
        month = printed[i].print_end_time.month
        year  = printed[i].print_end_time.year

        date = str(day) + ' / ' + str(month) + ' / ' + str(year)
        printed[i].endDate = date

    context = {'Quota'   : '00:31:23',
               'Jobs'    : prints,
               'Printed' : printed,
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
    printData = list(Job.objects.filter(job_id=jobid))

    for i in range(0, len(printData)):
        printData[i].uploadDate = str(printData[i].upload_time.day)      + ' / ' + str(printData[i].upload_time.month)      + ' / ' + str(printData[i].upload_time.year)
        printData[i].startDate  = str(printData[i].print_start_time.day) + ' / ' + str(printData[i].print_start_time.month) + ' / ' + str(printData[i].print_start_time.year)
        printData[i].endDate    = str(printData[i].print_end_time.day)   + ' / ' + str(printData[i].print_end_time.month)   + ' / ' + str(printData[i].print_end_time.year)

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


#Login views
def Login(request):
    context = {'Quota' : '00:31:23'}
    return render(request, 'Login.html', context)

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


#Layout
def Layout(request):
    context = {'Quota' : '00:31:23'}
    return render(request, 'Layout.html', context)


#Errors
#def error_404_view(request, exception):
#    context = {'Quota' : '00:31:23',}
#    return render(request, '404.html', context)

#def error_500_view(request, exception):
#    context = {'Quota' : '00:31:23',}
#    return render(request, '500.html', context)
