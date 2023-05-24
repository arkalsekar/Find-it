from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Job(models.Model):
    company_name = models.CharField(max_length=100, blank=True, null=True, default="My Company")
    title = models.CharField(max_length=100, blank=True, null=True, default="Developer")
    job_description = models.CharField(max_length=500, blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    interested_jobs = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    techonologies = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return str(self.username)
    

    