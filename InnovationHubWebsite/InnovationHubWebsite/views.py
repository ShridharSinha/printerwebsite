from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import os
from django.conf import settings

from .models import *
from .Util import *
from .CustomExceptions import *
from datetime import *
import pytz

import json


# Create your views here.
MONTHLY_QUOTA = 3600
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

    users = {
        'User'  : list(Profile.objects.all()),
        'Votes' : [],
    }

    for user in users.get('User'):
        vote_num = 0
        jobs = list(FeaturedPrint.objects.all())

        for i in range(len(jobs) -1, -1, -1):
            #print(jobs[i].fk_job.print_start_time.month)
            if(jobs[i].fk_job.print_start_time.month == datetime.now().month and jobs[i].fk_job.fk_profile == user):
            #if(jobs[i].fk_job.fk_profile == user):
                vote_num = vote_num + jobs[i].votes.count()
        users.get('Votes').append(vote_num)

    for i in range(0, len(users.get('User'))):
        for j in range(0, len(users.get('User')) - i - 1):
            if(users.get('Votes')[j] < users.get('Votes')[j + 1]):

                temp = users.get('Votes')[j]
                users.get('Votes')[j] = users.get('Votes')[j + 1]
                users.get('Votes')[j + 1] = temp

                temp = users.get('User')[j]
                users.get('User')[j] = users.get('User')[j + 1]
                users.get('User')[j + 1] = temp

    if(len(users.get('User')) > 10):
        for i in range(len(users.get('User'))-1, 9, -1):
            users.get('User').pop()
            users.get('Votes').pop()

    context['TopUsersMonth'] = []

    for i in range(0, len(users.get('User'))):
        context.get('TopUsersMonth').append({'User' : users.get('User')[i],
                                             'ID'   : str(i + 1),
                                            })


    users = {
        'User'  : list(Profile.objects.all()),
        'Votes' : [],
    }

    for user in users.get('User'):
        vote_num = 0
        jobs = list(FeaturedPrint.objects.all())

        for i in range(len(jobs) -1, -1, -1):
            #print(jobs[i].fk_job.print_start_time.month)
            if(jobs[i].fk_job.print_start_time.year == datetime.now().year and jobs[i].fk_job.fk_profile == user):
            #if(jobs[i].fk_job.fk_profile == user):
                vote_num = vote_num + jobs[i].votes.count()
        users.get('Votes').append(vote_num)

    for i in range(0, len(users.get('User'))):
        for j in range(0, len(users.get('User')) - i - 1):
            if(users.get('Votes')[j] < users.get('Votes')[j + 1]):

                temp = users.get('Votes')[j]
                users.get('Votes')[j] = users.get('Votes')[j + 1]
                users.get('Votes')[j + 1] = temp

                temp = users.get('User')[j]
                users.get('User')[j] = users.get('User')[j + 1]
                users.get('User')[j + 1] = temp

    if(len(users.get('User')) > 10):
        for i in range(len(users.get('User'))-1, 9, -1):
            users.get('User').pop()
            users.get('Votes').pop()

    context['TopUsersYear'] = []

    for i in range(0, len(users.get('User'))):
        context.get('TopUsersYear').append({'User' : users.get('User')[i],
                                            'ID'   : str(i + 1),
                                           })



    #context['TopPrints'] = list(Profile.objects.all())

    best_print_month = list(FeaturedPrint.objects.all())
    for i in range(len(best_print_month) - 1, -1, -1):
        if(not(best_print_month[i].fk_job.print_start_time.month == datetime.now().month)):
            best_print_month.pop(i)

    for i in range(0, len(best_print_month) - 1):
        if(best_print_month[0].votes.count() > best_print_month[1].votes.count()):
            best_print_month.pop(1)
        else:
            best_print_month.pop(0)

    best_print_year = list(FeaturedPrint.objects.all())
    for i in range(len(best_print_year) - 1, -1, -1):
        if(not(best_print_year[i].fk_job.print_start_time.year == datetime.now().year)):
            best_print_year.pop(i)

    for i in range(0, len(best_print_year) - 1):
        if(best_print_year[0].votes.count() > best_print_year[1].votes.count()):
            best_print_year.pop(1)
        else:
            best_print_year.pop(0)

    #context['BestPrintMonth'] = list(Job.objects.filter(job_id = 20))
    context['BestPrintMonth'] = best_print_month
    #context['BestPrintYear' ] = list(Job.objects.filter(job_id = 20))
    context['BestPrintYear' ] = best_print_year

    if(request.user.is_authenticated):
        context['authenticated'] = 'true'

    #month = util.getCurrentMonth()

    num_active      = util.getActiveUserNum()
    num_very_active = util.getVeryActiveUserNum()

    #profiles = list(Profile.objects.all())
    #for i in range(len(profiles), 0):
    #    if(profiles[i].quota < MONTHLY_QUOTA and not(profile.fk_user.is_superuser)):
    #        num_active = num_active + 1
    #    if(profiles[i].quota == 0 and not(profile.fk_user.is_superuser)):
    #        num_very_active = num_very_active + 1

    #num_active      = len(list(Profile.objects.filter(quota = MONTHLY_QUOTA))) - super_user_num
    #num_very_active = len(list(Profile.objects.filter(quota=0)))               - super_user_num

    month    = util.getCurrentMonth()
    objects  = list(Statistic.objects.filter(month_name = month))
    if(len(objects) > 0):
        Statistic_obj = objects[0]

        Statistic_obj.active_users_num      = num_active
        Statistic_obj.very_active_users_num = num_very_active
        Statistic_obj.save()

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
    util = Util()
    saved = False
    error_message = 'a'
    try:
        if request.method == 'POST':

            if(not(request.user.is_superuser) and util.getProfile(request.user).quota <= 0):
                error_message = 'Sorry, your print quota is over...  Try again next month.'
                raise NoRemainingQuotaException


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
            saved = True
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

            month    = util.getCurrentMonth()
            objects  = list(Statistic.objects.filter(month_name = month))
            if(len(objects) > 0):
                Statistic_obj = objects[0]
                #Statistic_obj.print_num                 = Statistic_obj.print_num + 1
                Statistic_obj.successful_submission_num = Statistic_obj.successful_submission_num + 1
                Statistic_obj.total_users_num           = len(list(User.objects.filter(is_superuser=False)))
                Statistic_obj.save()
                #print(Statistic_obj)


            #return HttpResponse("Submission Form")
            return redirect("success/")
        else:
            month    = util.getCurrentMonth()
            objects  = list(Statistic.objects.filter(month_name = month))
            if(len(objects) > 0):
                Statistic_obj = objects[0]
                Statistic_obj.failed_submission_num = Statistic_obj.failed_submission_num + 1
                Statistic_obj.save()
            return redirect('fail/')
    except Exception as e:
        #print(e)
        month    = util.getCurrentMonth()
        objects  = list(Statistic.objects.filter(month_name = month))
        if(len(objects) > 0):
            Statistic_obj = objects[0]
            Statistic_obj.failed_submission_num = Statistic_obj.failed_submission_num + 1
            Statistic_obj.save()
        if(saved):
            Job.objects.filter(job_id = newJob.job_id).delete()
        return redirect('fail/' + error_message)

@login_required(login_url='/login/')
def Success(request):
    util = Util()

    context = util.getQuota(request.user)
    #return HttpResponse("Submission Success")
    return render(request, 'SubmissionSuccess.html', context)

@login_required(login_url='/login/')
def Fail(request, error):
    util = Util()

    context = util.getQuota(request.user)
    context['error_message'] = error
    #return HttpResponse("Submission Fail")
    return(render(request, 'SubmissionFailed.html', context))

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

    videos = Video.objects.all()

    context['mainVideos']  = list(videos.filter(title='Introduction')) #[{'title':'Introduction', 'subtitle': '\"Aim for the stars...\"'}]

    context['userVideos']  = list(videos.filter(admin_only=False)) #[{'title':'The Home Page', 'subtitle': 'Part 1'},
                              #{'title':'The Submit Page', 'subtitle': 'Part 2'},
                              #{'title':'The Home Page', 'subtitle': 'Part 1'},
                              #{'title':'The Submit Page', 'subtitle': 'Part 2'},
                              #{'title':'The Home Page', 'subtitle': 'Part 1'},
                              #{'title':'The Submit Page', 'subtitle': 'Part 2'},]
    for i in range(len(context.get('userVideos')) - 1, -1, -1):
        if(context.get('userVideos')[i].title == 'Introduction'):
            context.get('userVideos').pop(i)

    for i in range(0, len(context.get('userVideos')) - 1):
        for j in range(0, len(context.get('userVideos')) - 1 - i):
            if(context.get('userVideos')[j].serial_num > context.get('userVideos')[j+1].serial_num):
                temp = context.get('userVideos')[j]
                context.get('userVideos')[j] = context.get('userVideos')[j+1]
                context.get('userVideos')[j+1] = temp


    context['adminVideos'] = list(videos.filter(admin_only=True)) #[{'title':'The Home Page', 'subtitle': 'Part 1'},
                              #{'title':'The Submit Page', 'subtitle': 'Part 2'},
                              #{'title':'The Home Page', 'subtitle': 'Part 1'},
                              #{'title':'The Submit Page', 'subtitle': 'Part 2'},
                              #{'title':'The Home Page', 'subtitle': 'Part 1'},
                              #{'title':'The Submit Page', 'subtitle': 'Part 2'},]
    for i in range(0, len(context.get('adminVideos')) - 1):
        for j in range(0, len(context.get('adminVideos')) - 1 - i):
            if(context.get('adminVideos')[j].serial_num > context.get('adminVideos')[j+1].serial_num):
                temp = context.get('adminVideos')[j]
                context.get('adminVideos')[j] = context.get('adminVideos')[j+1]
                context.get('adminVideos')[j+1] = temp

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
        #print("FAIL DOWN")
        x = 1

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

def ResetQuota(request):
    profiles = list(Profile.objects.all())
    for profile in profiles:
        if(not profile.user.is_superuser):
            if(profile.quota < MONTHLY_QUOTA):
                profile.quota = MONTHLY_QUOTA

        profile.save()
    return(HttpResponse("Success"))

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

        statistics = list(Statistic.objects.all())

        for i in range(0, len(statistics) - 1):
            for j in range(0, len(statistics) - 1 - i):
                if(statistics[j].month_num > statistics[j+1].month_num):
                    temp            = statistics[j]
                    statistics[j]   = statistics[j+1]
                    statistics[j+1] = temp


        month    = util.getCurrentMonth()
        objects  = list(Statistic.objects.filter(month_name = month))
        if(len(objects) > 0):
            Statistic_obj = objects[0]
            Statistic_obj.total_users_num       = len(list(User.objects.filter(is_superuser=False)))
            Statistic_obj.active_users_num      = util.getActiveUserNum()
            Statistic_obj.very_active_users_num = util.getVeryActiveUserNum()
            Statistic_obj.save()

        labels                 = []
        print_num              = []
        total_print_time       = []
        av_print_time          = []

        total_wait_time        = []
        av_wait_time           = []

        total_users            = []
        active_users           = []
        very_active_users      = []

        successful_submissions = 0
        failed_submissions     = 0

        for stat in statistics:
            labels.append(stat.month_name)

            print_num.append(stat.print_num)
            total_print_time.append(stat.print_time)

            total_wait_time.append(stat.wait_time)

            total_users.append(stat.total_users_num)
            active_users.append(stat.active_users_num)
            very_active_users.append(stat.very_active_users_num)

            successful_submissions = successful_submissions + stat.successful_submission_num
            failed_submissions     = failed_submissions     + stat.failed_submission_num

        for i in range(0, len(print_num)):
            if(print_num[i] != 0):
                av_print_time.append(total_print_time[i]/print_num[i])
                av_wait_time.append(total_wait_time[i]/print_num[i])
            else:
                av_print_time.append(0)
                av_wait_time.append(0)


        #for i in range(1, 6):
        context.get('charts').append({'No'      : '1',
                                      'Title'   : 'Number of Prints',
                                      'Subtitle': 'and Average Print Time',
                                      'Type'    : 'bar',
                                      'Labels'  : labels, # Dummy: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                                      'Data'    : [print_num, av_print_time], # Dummy: [[25, 34, 90, 78, 45, 67, 142, 123, 109, 87, 75, 23],[65, 94, 200, 178, 145, 167, 234, 232, 209, 187, 175, 83]],
                                      'Keys'     :["No. of Prints", "Average Print Time"],
                                      'CutOut'  : 0,
                                     });

        context.get('charts').append({'No'      : '2',
                                      'Title'   : 'Average Wait Time',
                                      'Subtitle': 'for Prints',
                                      'Type'    : 'bar',
                                      'Labels'  : labels, # Dummy: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                                      'Data'    : [av_wait_time], # Dummy: [[65, 94, 200, 178, 145, 167, 234, 232, 209, 187, 175, 83]],
                                      'Keys'     :["Average Wait Time"],
                                      'CutOut'  : 0,
                                     });

        context.get('charts').append({'No'      : '3',
                                      'Title'   : 'User Activity',
                                      'Subtitle': 'Number of Active Users',
                                      'Type'    : 'line',
                                      'Labels'  : labels, # Dummy: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                                      'Data'    : [very_active_users, active_users, total_users],# Dummy: [[25, 34, 90, 78, 45, 67, 142, 123, 109, 87, 75, 23],[65, 94, 200, 178, 145, 167, 234, 232, 209, 187, 175, 83], [400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]],
                                      'Keys'    : ["Very Active Users", "Active Users", "Total Number of Users"],
                                      'CutOut'  : 0,
                                     });

        context.get('charts').append({'No'      : '4',
                                      'Title'   : 'Print Submission',
                                      'Subtitle': 'Success Rate',
                                      'Type'    : 'pie',
                                      'Labels'  : ['Success', 'Failure'],
                                      'Data'    : [[successful_submissions, failed_submissions]], # Dummy: [[54, 8]],
                                      'Keys'     :["Success", "Failure"],
                                      'CutOut'  : 50,
                                     });

        #context['chart_data'] = []

        #for i in range(0, len(context.get('charts'))):
            #context.get('chart_data').append(json.dumps(context.get('charts')[i]))


        return render(request, 'Statistics.html', context)
    else:
        return redirect('/infidel/')

@login_required(login_url='/infidel/')
def ClearStatistics(request):
    if(request.user.is_superuser):
        util = Util()
        util.clearStatistics()

        return HttpResponse("Statistics Cleared")
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

        for i in range(0, len(current)):
            for j in range(0, len(current) - 1 - i):
                if(current[j].job_id > current[j+1].job_id):
                    temp         = current[j]
                    current[j]   = current[j+1]
                    current[j+1] = temp

        for i in range(0, len(inQueue)):
            for j in range(0, len(inQueue) - 1 - i):
                if(inQueue[j].job_id > inQueue[j+1].job_id):
                    temp         = inQueue[j]
                    inQueue[j]   = inQueue[j+1]
                    inQueue[j+1] = temp

        context['inQueue'] = inQueue

        return render(request, 'Printer.html', context)
    else:
        return redirect('/infidel/')

@login_required(login_url='/infidel/')

def Printed(request, jobid):
    if(request.user.is_superuser):
        util = Util()
        jobs = list(Job.objects.filter(job_id = jobid))
        if(len(jobs) == 1):

            job = jobs[0]
            job.status = "Printed"
            time = int(request.GET['job_time'])
            job.print_time = str(time)

            job.print_end_time = datetime.now();

            profile = job.fk_profile# -= time
            initial_quota = profile.quota
            has_become_active = initial_quota >= MONTHLY_QUOTA
            profile.quota = profile.quota - time

            #has_become_very_active = False
            #if(profile.quota < 0):
            #    profile.quota = 0
            #    if(initial_quota > 0):
            #        has_become_very_active = True

            num_active      = util.getActiveUserNum()
            num_very_active = util.getVeryActiveUserNum()

            #profiles = list(Profile.objects.all())

            #for i in range(len(profiles), 0):
            #    if(profiles[i].quota < MONTHLY_QUOTA and not(profile.fk_user.is_superuser)):
            #        num_active = num_active + 1
            #    if(profiles[i].quota == 0 and not(profile.fk_user.is_superuser)):
            #        num_very_active = num_very_active + 1

            #num_active      = len(list(Profile.objects.filter(quota = MONTHLY_QUOTA))) - super_user_num
            #num_very_active = len(list(Profile.objects.filter(quota=0)))               - super_user_num



            job.save()

            profile.save()

            month    = util.getCurrentMonth()
            objects  = list(Statistic.objects.filter(month_name = month))
            if(len(objects) > 0):
                Statistic_obj            = objects[0]
                Statistic_obj.print_num  = Statistic_obj.print_num  + 1
                Statistic_obj.print_time = Statistic_obj.print_time + time

                wait = job.wait_time
                Statistic_obj.wait_time = Statistic_obj.wait_time + wait
                #if(has_become_active):
                #    Statistic_obj.active_users_num = Statistic_obj.active_users_num + 1
                #if(has_become_very_active):
                #    Statistic_obj.very_active_users_num = Statistic_obj.very_active_users_num + 1

                Statistic_obj.active_users_num      = num_active
                Statistic_obj.very_active_users_num = num_very_active

                #print("Success!")
                Statistic_obj.save()

            return HttpResponse('success')

    else:
        return redirect('/infidel/')

def Printing(request, jobid):
    if(request.user.is_superuser):
        jobs = list(Job.objects.filter(job_id = jobid))
        if(len(jobs) == 1):

            job = jobs[0]
            job.status = "Printing"
            job.print_start_time = datetime.now()

            #now_aware = unaware.replace(tzinfo=pytz.UTC)
            time_a = job.print_start_time.replace(tzinfo=pytz.UTC)
            time_b = job.upload_time.replace(tzinfo=pytz.UTC)
            delta_time = time_a - time_b
            wait_in_seconds = delta_time.total_seconds()

            job.wait_time = wait_in_seconds

            job.save()

            #path = '/printer/' + job.printer_name
            return redirect('/printData/download/' + str(jobid))

    else:
        return redirect('/infidel/')


def Infidel(request):
    return HttpResponse("This is the grown up's table! It's not for sneaky idiots like you!<br>I've got to say though, nice try!<br>But now it's time for bed.<br><br>GO <a href='/home'>Home</a>!!!")



#AboutUs
def AboutUs(request):
    util = Util()
    context = util.getQuota(request.user)
    return(render(request, 'AboutUs.html', context))

#Errors
#def error_404(request, exception):
    #util = Util()
    #context = util.getQuota()

    ##context['Error']         = '404'
    ##context['error_message'] = 'The page you are looking for doesn\'t seem to exist. Please return to the Home Page.'
    #return render(request, '404.html', context)

#def error_500_view(request, exception):
#    context = {'Quota' : '00:31:23',}
#    return render(request, '500.html', context)


#handler404 = 'InnovationHubWebite.views.error_404'
