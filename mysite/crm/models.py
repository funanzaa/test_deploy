import os
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Project_subgroup(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Hospitals(models.Model):
    CATEGORY = (
        ('1','โรงพยาบาล'),
        ('3','ศูนย์บริการสาธารณสุข'),
        ('4','คลินิก'),
    )
    h_type = models.CharField(max_length=255, choices=CATEGORY)
    label = models.CharField(max_length=255)
    code = models.CharField(max_length=255,null=True)
    date_created = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('label', 'code')

    def __str__(self):
        return self.code + " : " + self.label

class Service(models.Model):
    CATEGORY = (
        ('call','call'),
        ('line','line'),
        ('facebook','facebook'),
        ('email','email'),
    )
    name = models.CharField(max_length=255,null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Case(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, null=True,on_delete= models.SET_NULL)
    project_subgroup = models.ForeignKey(Project_subgroup, null=True,on_delete= models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, on_delete= models.SET_NULL)
    resolution = models.TextField()
    service = models.ForeignKey(Service, null=True, on_delete= models.SET_NULL)
    hospitals = models.ForeignKey(Hospitals, null=True, on_delete= models.SET_NULL)
    date_entered = models.DateTimeField(null=True, blank=True)
    update_at =  models.DateTimeField(null=True, blank=True)
    case_pic = models.ImageField(blank=True)

    def __str__(self):
        return self.name
