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
    #fk_user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fk_job =models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    votes  =models.IntegerField()

    #ERRORY LINE
    #def __str__(self):
    #    name = ''
    #    for n in FeaturedPrint.objects.raw('SELECT job_title FROM FeaturedPrint , Job WHERE FeaturedPrint.fk_job = Job.job_id;'):
    #        name = n
    #    return(name)

    #def __str__(self):
    #    job = FeaturedPrint.objects.filter(job_id = self.fk_job).select_related()
    #    return(job.job_title)

    def __str__(self):
        return(self.fk_job.__str__())


class RecentPrint(models.Model):
    #fk_user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fk_job =models.ForeignKey(Job, on_delete=models.CASCADE, null=True)

    #def __str__(self):
