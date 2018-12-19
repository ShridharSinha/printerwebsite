from django.db import models
from vote.models import VoteModel
from django.contrib.auth.models import User


class Profile(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    quota     = models.IntegerField()
    grade     = models.IntegerField(null=True)
    section   = models.CharField(max_length=10, null=True)

    def __str__(self):
        name = ""
        if(self.user.first_name != ""):
            name = self.user.first_name + " " + self.user.last_name
        else:
            name = self.user.username
        return(name)

    def equals(self, user):
        equality = (user.id == self.user.id)
        return(equality)

    def equalsProfile(self, profile):
        return(profile.id == self.id)


class Job(models.Model):
    job_id          =models.AutoField(primary_key=True)
    job_title       =models.CharField(max_length=500)
    status          =models.CharField(max_length=20)             #in Queue, Printing, Printed
    colour          =models.CharField(max_length=10, null=True)
    upload_time     =models.DateTimeField(null=True)
    print_start_time=models.DateTimeField(null=True)
    print_end_time  =models.DateTimeField(null=True)
    print_time      =models.CharField(max_length=20, null=True)
    wait_time       =models.IntegerField(null=True)
    printer_name    =models.CharField(max_length=20, null=True)
    fk_profile      =models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    file_path_stl   =models.CharField(max_length=1000, null=True)
    file_path_obj   =models.CharField(max_length=1000, null=True)
    special_marker  =models.CharField(max_length=20, null=True)

    uploadDate = ''
    startDate = ''
    endDate = ''

    def __str__(self):
        return(self.job_title)

    def getStatus(self):
        return(self.status)


class FeaturedPrint(VoteModel, models.Model):
    #print_id =models.AutoField(primary_key=True)
    fk_job   =models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    #votes    =models.IntegerField()

    def __str__(self):
        return(self.fk_job.__str__())


class RecentPrint(models.Model):
    #fk_user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fk_job =models.ForeignKey(Job, on_delete=models.CASCADE, null=True)

    #def __str__(self):

class Statistic(models.Model):
    month_num                 =models.IntegerField(null=True)
    month_name                =models.CharField(max_length=30)
    print_num                 =models.IntegerField()
    print_time                =models.IntegerField()
    wait_time                 =models.IntegerField()
    successful_submission_num =models.IntegerField()
    failed_submission_num     =models.IntegerField()
    total_users_num           =models.IntegerField(null=True)
    active_users_num          =models.IntegerField(null=True)
    very_active_users_num     =models.IntegerField(null=True)

    def __str__(self):
        return(self.month_name)

    def clear(self):
        #self.month_name                = 0
        self.print_num                 = 0
        self.print_time                = 0
        self.wait_time                 = 0
        self.successful_submission_num = 0
        self.failed_submission_num     = 0
        self.total_users_num           = 0
        self.active_users_num          = 0
        self.very_active_users_num     = 0
