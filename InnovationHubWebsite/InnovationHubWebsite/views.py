from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import *
from .Util import *
from datetime import *


# Create your views here.

#HomePage Views
def HomePage(request):
    util = Util()

    context = util.getQuota(request.user)

    context['FeaturedPrint'] = list(FeaturedPrint.objects.all())

    for i in range(0, len(context.get('FeaturedPrint'))):
        for j in range(0, len(context.get('FeaturedPrint')) - i - 1):
            if(context.get('FeaturedPrint')[j].votes < context.get('FeaturedPrint')[j + 1].votes):
                temp = context.get('FeaturedPrint')[j]
                context.get('FeaturedPrint')[j] = context.get('FeaturedPrint')[j + 1]
                context.get('FeaturedPrint')[j + 1] = temp

    for i in range(3, len(context.get('FeaturedPrint'))):
        context.get('FeaturedPrint').pop()

    #profiles = list(Profile.objects.all())
    #context['TopPrints'] = {'Profiles': [],
                            #'Numbers' : [],
                            #}
    #for i in range(1, len(profiles) + 1):
    #    context['TopPrints']['Profiles'].append(profiles[i - 1])
    #    context['TopPrints']['Numbers'].append(i + 1)

    context['TopPrints'] = list(Profile.objects.all())

    context['BestPrintMonth'] = list(Job.objects.filter(job_id = 20))
    context['BestPrintYear' ] = list(Job.objects.filter(job_id = 20))

    return render(request, 'HomePage.html', context)



#Schedule Views
@login_required(login_url='/login/')
def Schedule(request):
    util = Util()

    prints = []
    printed = []
    if request.user.is_superuser:
        inQueue  = list(Job.objects.filter(status = "in Queue"))
        printing = list(Job.objects.filter(status = "Printing"))

        for i in range(0, len(inQueue)):
            prints.append(inQueue[i])

        for i in range(0, len(printing)):
            prints.append(printing[i])

        printed  = list(Job.objects.filter(status = "Printed"))

    else:
        inQueue  = list(Job.objects.filter(status = "in Queue").filter(fk_profile = util.getProfile(request.user)))
        printing = list(Job.objects.filter(status = "Printing"))

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

    util = Util()

    context = util.getQuota(request.user)

    context['Jobs'] = prints
    context['Printed'] = printed

    #for i in range(0, len(prints)):
        #context["Job"    + str(i)] = prints[i].__str__()
        #context["Status" + str(i)] = prints[i].status
    return render(request, 'SchedulePage.html', context)



#Submit Views
@login_required(login_url='/login/')
def Submission(request):
    util = Util()

    context = util.getQuota(request.user)

    return render(request, 'SubmitFile.html', context)

@login_required(login_url='/login/')
def Preview(request):
    return HttpResponse("Preview your model")

@login_required(login_url='/login/')
def SubmissionRequest(request):
    try:
        if request.method == 'POST':

            newJob = Job()
            util   = Util()

            newJob.job_title = request.POST['printName']
            newJob.colour    = request.POST['colour']

            #pathSTL, pathOBJ = util.handle_file(request.FILES['file'], request.POST.get('printName'), request.user)
            #newJob.file_path_stl = pathSTL
            #newJob.file_path_obj = pathOBJ

            newJob.status           = 'in Queue'
            newJob.upload_time      = datetime.now()
            newJob.print_start_time = util.getPrintStartTime()
            newJob.print_end_time   = util.getPrintEndTime(request.FILES['file'])
            newJob.fk_profile       = util.getProfile(request.user)
            newJob.printer_name     = util.getPrinterName();


            newJob.save()

            pathSTL, pathOBJ = util.handle_file(request.FILES['file'], request.POST['printName'], request.user, newJob.job_id)
            newJob.file_path_stl = pathSTL
            newJob.file_path_obj = pathOBJ

            newJob.save()

            #return HttpResponse("Submission Form")
            return redirect("success/")
        else:
            return redirect('fail/')
    except:
        return redirect('fail/')

@login_required(login_url='/login/')
def Success(request):
    util = Util()

    context = util.getQuota(request.user)
    return HttpResponse("Submission Success")

@login_required(login_url='/login/')
def Fail(request):
    util = Util()

    context = util.getQuota(request.user)
    return HttpResponse("Submission Fail")

@login_required(login_url='/login/')
def PrintData(request, jobid):
    printData = list(Job.objects.filter(job_id=jobid))

    for i in range(0, len(printData)):
        printData[i].uploadDate = str(printData[i].upload_time.day)      + ' / ' + str(printData[i].upload_time.month)      + ' / ' + str(printData[i].upload_time.year)
        printData[i].startDate  = str(printData[i].print_start_time.day) + ' / ' + str(printData[i].print_start_time.month) + ' / ' + str(printData[i].print_start_time.year)
        printData[i].endDate    = str(printData[i].print_end_time.day)   + ' / ' + str(printData[i].print_end_time.month)   + ' / ' + str(printData[i].print_end_time.year)

    util = Util()

    context = util.getQuota(request.user)
    context['JobData'] = printData

    return render(request, 'PrintData.html', context)



#Account Views
@login_required(login_url='/login/')
def AccountData(request):
    util = Util()

    context = util.getQuota(request.user)
    context['name']  = util.getProfile(request.user).__str__()
    context['class'] = util.getProfile(request.user).section

    return render(request, 'AccountData.html', context)

@login_required(login_url='/login/')
def EditAccount(request):
    return HttpResponse("Account Editor")

@login_required(login_url='/login/')
def Login(request):
    return HttpResponse("Login to Account")

#@login_required(login_url='/login/')
#def layout(request):
#    context = {'Quota' : '00:31:23'}

#    if request.user.is_authenticated():
#        context['LogButton'] = 'LOGOUT'
#    else:
#        context['LogButton'] = 'LOGIN'

#    return render(request, 'layout.html', context)



#The Carl Segment
def CarlPage(request):
    util = Util()

    context = util.getQuota(request.user)
    return render(request, 'CarlSegment.html', context)


#Login views
def Login(request):
    util = Util()

    context = util.getQuota(request.user)
    context['next'] = request.GET.get('next')

    return render(request, 'Login.html', context)


def Authenticate(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username = username, password = password)

    next = request.POST['next']

    if user is not None:
        login(request, user)
        return redirect(next)
    else:
        return redirect('/login/?next=/home/')
    #return HttpResponse("Auth")

def Logout(request):
    logout(request)
    return redirect('/login/')

#Featured Prints
def Featured(request):
    util = Util()

    context = util.getQuota(request.user)
    context['Jobs'] = list(FeaturedPrint.objects.all())

    for i in range(0, len(context.get('Jobs'))):
        for j in range(0, len(context.get('Jobs')) - i - 1):
            if(context.get('Jobs')[j].votes < context.get('Jobs')[j + 1].votes):
                temp = context.get('Jobs')[j]
                context.get('Jobs')[j] = context.get('Jobs')[j + 1]
                context.get('Jobs')[j + 1] = temp

    return render(request, 'FeaturedPrints.html', context)


#Layout
def Layout(request):
    util = Util()

    context = util.getQuota(request.user)

    return render(request, 'Layout.html', context)


#ADMIN
@login_required(login_url='/infidel/')
def AdminHome(request):
    if(request.user.is_superuser):
        context = {}
        return render(request, 'Admin.html', context)
    else:
        return redirect('/infidel/')
        #return HttpResponse("This is the grown up's table! It's not for sneaky idiots like you!")

def Infidel(request):
    return HttpResponse("This is the grown up's table! It's not for sneaky idiots like you!")


#Errors
#def error_404_view(request, exception):
#    context = {'Quota' : '00:31:23',}
#    return render(request, '404.html', context)

#def error_500_view(request, exception):
#    context = {'Quota' : '00:31:23',}
#    return render(request, '500.html', context)
