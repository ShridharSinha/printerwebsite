from django.db import models


class User(models.Model):
    user_id   =models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name =models.CharField(max_length=50)
    quota     =models.IntegerField()

    def __str__(self):
        name = self.first_name + " " + self.last_name
        return(name)


class Job(models.Model):
    job_id          =models.AutoField(primary_key=True)
    job_title       =models.CharField(max_length=50)
    status          =models.CharField(max_length=20)
    upload_time     =models.DateTimeField(null=True)
    print_start_time=models.DateTimeField(null=True)
    print_end_time  =models.DateTimeField(null=True)
    printer_name    =models.CharField(max_length=20, null=True)
    fk_user         =models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    file_path       =models.CharField(max_length=50, null=True)

    def __str__(self):
        return(self.job_title)


class FeaturedPrint(models.Model):
    fk_user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fk_job =models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    votes  =models.IntegerField()
    

class RecentPrint(models.Model):
    fk_user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fk_job =models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
