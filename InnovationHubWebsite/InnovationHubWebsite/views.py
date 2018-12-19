from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import os
from django.conf import settings

from .models import *
from .Util import *
from datetime import *

import json


# Create your views here.

#HomePage Views
def HomePage(request):
    util = Util()

    context = util.getQuota(request.user)

    context['FeaturedPrint'] = list(FeaturedPrint.objects.all())

    for i in range(0, len(context.get('FeaturedPrint'))):
        for j in range(0, len(context.get('FeaturedPrint')) - i - 1):
            if(context.get('FeaturedPrint')[j].votes.count() < context.get('FeaturedPrint')[j + 1].votes.count()):
                temp = context.get('FeaturedPrint')[j]
                context.get('FeaturedPrint')[j] = context.get('FeaturedPrint')[j + 1]
                context.get('FeaturedPrint')[j + 1] = temp

    for i in range(3, len(context.get('FeaturedPrint'))):
        context.get('FeaturedPrint').pop()

    if(len(context['FeaturedPrint']) < 3):
        context['Featured'] = False
    else:
        context['Featured'] = True
    if(len(context.get('FeaturedPrint')) > 2):
        context['FeaturedPrint0'] = context.get('FeaturedPrint')[0]
        context['FeaturedPrint1'] = context.get('FeaturedPrint')[1]
        context['FeaturedPrint2'] = context.get('FeaturedPrint')[2]

    for i in range(0, len(context.get('FeaturedPrint'))):
        job = context.get('FeaturedPrint' + str(i))
        context.get('FeaturedPrint')[i] = {'Job'       : job,
                                           'VoteStatus': job.votes.exists(request.user.id),
                                           }

    #for i in range(0,3):
        #context.get('FeaturedPrint' + str(i)).annotate(num_votes = Count('votes__user'))

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

    if(request.user.is_authenticated):
        context['authenticated'] = 'true'

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
        printing = list(Job.objects.filter(status = "Printing").filter(fk_profile = util.getProfile(request.user)))

        for i in range(0, len(inQueue)):
            prints.append(inQueue[i])

        for i in range(0, len(printing)):
            prints.append(printing[i])

        printed  = list(Job.objects.filter(status = "Printed").filter(fk_profile = util.getProfile(request.user)))

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

    if(len(printed) >= 3):
        context['Recent']       = True
        context['RecentPrints0'] = printed[0]
        context['RecentPrints1'] = printed[1]
        context['RecentPrints2'] = printed[2]
    else :
        context['Recent'] = False

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
            #jobs = list(Job.objects.all())
            #id = 0
            #if(len(jobs) == 0):
            #    id = 0
            #for i in range(0, len(jobs)):
            #    if(jobs[i].job_id > id):
            #        id = jobs[i].job_id

            #id =


            pathSTL, pathOBJ = util.handle_file(request.FILES['file'], request.POST['printName'], request.user, newJob.job_id)
            newJob.file_path_stl = pathSTL
            newJob.file_path_obj = pathOBJ

            newJob.save()

            #return HttpResponse("Submission Form")
            return redirect("success/")
        else:
            return redirect('fail/')
    except Exception as e:
        print(e)
        Job.objects.filter(job_id = newJob.job_id).delete()
        return redirect('fail/')

@login_required(login_url='/login/')
def Success(request):
    util = Util()

    context = util.getQuota(request.user)
    #return HttpResponse("Submission Success")
    return render(request, 'SubmissionSuccess.html', context)

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

    printData = list(Job.objects.filter(job_id=jobid))

    context['filePath'] = "/" + printData[0].file_path_stl
    context['jobid']    = jobid

    return render(request, 'PrintData.html', context)

def PrintDownload(request, jobid):
    #context = {}
    printData = list(Job.objects.filter(job_id=jobid))
    file_name = printData[0].file_path_stl

    response = HttpResponse(open(file_name, 'rb').read())
    response['Content-Type'] = 'application/sla'
    response['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return(response)




#Account Views
@login_required(login_url='/login/')
def AccountData(request):
    util = Util()

    context = util.getQuota(request.user)
    context['name']  = util.getProfile(request.user).__str__()
    context['class'] = str(util.getProfile(request.user).grade) + util.getProfile(request.user).section

    #if request.user.is_superuser:
    #    printed  = list(Job.objects.filter(status = "Printed"))
    #else:
    #    printed  = list(Job.objects.filter(status = "Printed").filter(fk_profile = util.getProfile(request.user)))
    if(not(request.user.is_superuser)):
        printed  = list(Job.objects.filter(status = "Printed").filter(fk_profile = util.getProfile(request.user)))
        if(len(printed) >= 3):
            context['Recent']       = True
            context['RecentPrints0'] = printed[0]
            context['RecentPrints1'] = printed[1]
            context['RecentPrints2'] = printed[2]
        else:
            context['Recent'] = False

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
            if(context.get('Jobs')[j].votes.count() < context.get('Jobs')[j + 1].votes.count()):
                temp = context.get('Jobs')[j]
                context.get('Jobs')[j] = context.get('Jobs')[j + 1]
                context.get('Jobs')[j + 1] = temp

    for i in range(0, len(context.get('Jobs'))):
        job = context.get('Jobs')[i]
        context.get('Jobs')[i] = {'Job'       : job,
                                  'VoteStatus': job.votes.exists(request.user.id),
                                 }

    context['num'] = len(context.get('Jobs'))

    context['hiddenVar'] = []#{'prints':[],
                             #'ids'   :[],}

    for i in range(1, len(context.get('Jobs')) + 1):
        var = {}
        #context.get('hiddenVar').get('ids').append('ModelName' + str(i))
        #context.get('hiddenVar').get('prints').append(context.get('Jobs')[i - 1])
        var['ids']    = 'modelName' + str(i)
        var['prints'] = context.get('Jobs')[i - 1]

        context.get('hiddenVar').append(var)

    #for i in range(0, context.get('Jobs')):
        #context.get('Jobs')[i].annotate(num_votes = Count('votes__user'))

    if(request.user.is_authenticated):
        context['authenticated'] = 'true'

    return render(request, 'FeaturedPrints.html', context)

@login_required(login_url='/login/')
def VoteUp(request, jobid):
    user = request.user


    #try:
    fPrint = list(FeaturedPrint.objects.filter(fk_job = list(Job.objects.filter(job_id = jobid))[0]))
    fPrint[0].votes.up(user.id)
    #except:
        #print("FAIL UP")

    return(HttpResponse("VoteUp"))

@login_required(login_url='/login/')
def VoteDown(request, jobid):
    user = request.user
    #fPrint = list(FeaturedPrint.objects.filter(fk_job = Job.objects.filter(job_id = jobid)))

    try:
        fPrint = list(FeaturedPrint.objects.filter(fk_job = list(Job.objects.filter(job_id = jobid))[0]))
        fPrint[0].votes.delete(user.id)
    except:
        print("FAIL DOWN")

    return(HttpResponse("VoteDown"))

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

@login_required(login_url='/infidel/')
def IncreaseGrade(request):
    if(request.user.is_superuser):
        util = Util()
        util.changeGrade(1)
        return redirect('/ADMIN/')
    else:
        return redirect('/infidel/')

@login_required(login_url='/infidel/')
def DecreaseGrade(request):
    if(request.user.is_superuser):
        util = Util()
        util.changeGrade(-1)
        return redirect('/ADMIN/')
    else:
        return redirect('/infidel/')

def AdminExcel(request):
    if(request.user.is_superuser):
        util = Util()
        context= util.getQuota(request.user)
        return render(request, 'AdminExcel.html', context)
    else:
        return redirect('/infidel/')


def ReturnStudentList(request):
    if(request.user.is_superuser):
        file_name = "Students.xls"

        util = Util()
        students = list(Profile.objects.all())

        studentData = []
        #print("Num Students:")
        #print(len(students))

        for i in range(0, len(students)):
            s = []
            s.append(str(i + 1))
            s.append(students[i].user.first_name)
            s.append(students[i].user.last_name)
            s.append(students[i].user.username)
            s.append(students[i].grade)
            s.append(students[i].section)
            s.append(students[i].quota)
            studentData.append(s)

        util.writeTo(file_name, studentData)

        #response = HttpResponse(content_type='application/ms-excel')
        #response['Content-Disposition'] = 'attachment;filename=%s' % file_name
        #response['X-sendfile'] = os.path.join(os.path.dirname(__file__), file_name)
        #print(response)
        #print(os.path.join(os.path.dirname(__file__), file_name))

        response = HttpResponse(open(file_name, 'rb').read())
        response['Content-Type'] = 'application/ms-excel'
        response['Content-Disposition'] = 'attachment;filename=%s' % file_name

        return(response)

    else:
        return redirect('/infidel/')

def ReturnJobList(request):
    if(request.user.is_superuser):
        file_name = "Jobs.xls"

        util = Util()
        jobs = list(Job.objects.all())

        jobData = []
        #print("Num Students:")
        #print(len(students))

        for i in range(0, len(jobs)):
            j = []
            j.append(str(i + 1))
            j.append(jobs[i].job_id)
            j.append(jobs[i].job_title)
            j.append(jobs[i].colour)
            j.append(jobs[i].upload_time)
            j.append(jobs[i].print_start_time)
            j.append(jobs[i].print_end_time)
            j.append(jobs[i].printer_name)
            j.append(jobs[i].fk_profile.user.username)
            j.append(jobs[i].file_path_stl)
            j.append(jobs[i].file_path_obj)
            j.append(jobs[i].special_marker)
            jobData.append(j)

        util.writeTo(file_name, jobData)

        #response = HttpResponse(content_type='application/ms-excel')
        #response['Content-Disposition'] = 'attachment;filename=%s' % file_name
        #response['X-sendfile'] = os.path.join(os.path.dirname(__file__), file_name)
        #print(response)
        #print(os.path.join(os.path.dirname(__file__), file_name))

        response = HttpResponse(open(file_name, 'rb').read())
        response['Content-Type'] = 'application/ms-excel'
        response['Content-Disposition'] = 'attachment;filename=%s' % file_name

        return(response)

    else:
        return redirect('/infidel/')


@login_required(login_url='/infidel/')
def Statistics(request):
    if(request.user.is_superuser):
        util = Util()
        context = util.getQuota(request.user)

        context['charts'] = []

        #for i in range(1, 6):
        context.get('charts').append({'No'      : '1',
                                      'Title'   : 'Number of Prints',
                                      'Subtitle': 'and Average Print Time',
                                      'Type'    : 'bar',
                                      'Labels'  : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                                      'Data'    : [[25, 34, 90, 78, 45, 67, 142, 123, 109, 87, 75, 23],[65, 94, 200, 178, 145, 167, 234, 232, 209, 187, 175, 83]],
                                      'Keys'     :["No. of Prints", "Average Print Time"],
                                      'CutOut'  : 0,
                                     });

        context.get('charts').append({'No'      : '2',
                                      'Title'   : 'Average Wait Time',
                                      'Subtitle': 'for Prints',
                                      'Type'    : 'bar',
                                      'Labels'  : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                                      'Data'    : [[65, 94, 200, 178, 145, 167, 234, 232, 209, 187, 175, 83]],
                                      'Keys'     :["Average Wait Time"],
                                      'CutOut'  : 0,
                                     });

        context.get('charts').append({'No'      : '3',
                                      'Title'   : 'User Activity',
                                      'Subtitle': 'Number of Active Users',
                                      'Type'    : 'line',
                                      'Labels'  : ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                                      'Data'    : [[25, 34, 90, 78, 45, 67, 142, 123, 109, 87, 75, 23],[65, 94, 200, 178, 145, 167, 234, 232, 209, 187, 175, 83], [400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]],
                                      'Keys'     :["Very Active Users", "Active Users", "Total Number of Users"],
                                      'CutOut'  : 0,
                                     });

        context.get('charts').append({'No'      : '4',
                                      'Title'   : 'Print Submission',
                                      'Subtitle': 'Success Rate',
                                      'Type'    : 'pie',
                                      'Labels'  : ['Success', 'Failure'],
                                      'Data'    : [[54, 8]],
                                      #'Keys'     :["Success", "Failure"],
                                      'CutOut'  : 50,
                                     });

        #context['chart_data'] = []

        #for i in range(0, len(context.get('charts'))):
            #context.get('chart_data').append(json.dumps(context.get('charts')[i]))


        return render(request, 'Statistics.html', context)
    else:
        return redirect('/infidel/')

@login_required(login_url='/infidel/')
def Printer(request, name):
    if(request.user.is_superuser):
        context = {'name':name,}

        current = list(Job.objects.filter(printer_name = name).filter(status = 'Printing'))
        if(len(current) > 0):
            context['current'] = current

            if(len(current) > 1):
                context['currentLen']  = len(current)

        inQueue = list(Job.objects.filter(printer_name = name).filter(status = 'in Queue'))
        context['inQueue'] = inQueue

        return render(request, 'Printer.html', context)
    else:
        return redirect('/infidel/')

@login_required(login_url='/infidel/')

def Printed(request, jobid):
    if(request.user.is_superuser):
        jobs = list(Job.objects.filter(job_id = jobid))
        if(len(jobs) == 1):

            job = jobs[0]
            job.status = "Printed"
            time = int(request.GET['job_time'])
            job.print_time = str(time)

            profile = job.fk_profile# -= time
            profile.quota = profile.quota - time

            if(profile.quota < 0):
                profile.quota = 0

            job.save()

            profile.save()

            return HttpResponse('success')

    else:
        return redirect('/infidel/')

def Printing(request, jobid):
    if(request.user.is_superuser):
        jobs = list(Job.objects.filter(job_id = jobid))
        if(len(jobs) == 1):

            job = jobs[0]
            job.status = "Printing"
            job.save()

            #path = '/printer/' + job.printer_name
            return redirect('/printData/download/' + str(jobid))

    else:
        return redirect('/infidel/')

#Errors
#def error_404_view(request, exception):
#    context = {'Quota' : '00:31:23',}
#    return render(request, '404.html', context)

#def error_500_view(request, exception):
#    context = {'Quota' : '00:31:23',}
#    return render(request, '500.html', context)

def Infidel(request):
    return HttpResponse("This is the grown up's table! It's not for sneaky idiots like you!<br>I've got to say though, nice try!<br>But now it's time for bed.<br><br>GO <a href='/home'>Home</a>!!!")



#AboutUs
def AboutUs(request):
    util = Util()
    context = util.getQuota(request.user)
    return(render(request, 'AboutUs.html', context))
