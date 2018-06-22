from django.db import models


class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    quota = models.IntegerField()

class Job(models.Model):
    job_id=models.AutoField(primary_key=True)
    job_title=models.CharField(max_length=50)
    status=models.CharField(max_length=20)
    upload_time=models.DateTimeField(null=True)
    print_start_time=models.DateTimeField(null=True)
    print_end_time=models.DateTimeField(null=True)
    printer_name=models.CharField(max_length=20, null=True)
    fk_user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    file_path=models.CharField(max_length=50, null=True)
