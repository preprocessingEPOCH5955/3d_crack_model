from typing import Any
from django.db import models
from datetime import datetime



class Signup_form(models.Model):
    firstname = models.CharField(max_length=30 , blank = True)
    lastname = models.CharField(max_length=30, blank = True)
    email = models.CharField(max_length=30, blank=True, unique=True)
    password = models.CharField(max_length=20, blank=True)
    project_name = models.CharField(max_length=30, blank = True)
    
    data_time = models.DateTimeField(default=datetime.now,blank=True)
    
    def __str__(self):
        return self.email


class project_data(models.Model):
    user = models.ForeignKey(Signup_form, on_delete=models.CASCADE, related_name='projects_data',null=True,unique=False)
    lon = models.CharField(null=True, max_length=10)
    lat = models.CharField(null=True,max_length=10)
    lid = models.CharField(null=True,max_length=10)
    result = models.CharField(null=True,max_length=10)
    face = models.CharField(max_length=10, blank=True )
    building_id = models.IntegerField()
