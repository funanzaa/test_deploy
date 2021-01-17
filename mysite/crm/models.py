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
    project = models.ForeignKey(Project, null=True,on_delete= models.SET_NULL) # add
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name + " : " + str(self.project)

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
    active = models.CharField(max_length=255)
    install_app = models.CharField(max_length=255)
    training = models.CharField(max_length=255)

    def __str__(self):
        return self.code + " : " + self.label

class Service(models.Model):
    name = models.CharField(max_length=255,null=True)
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


class ControlVersion(models.Model):
    hcode = models.CharField(max_length=140, default='')
    app_controlVersion = models.CharField(max_length=255)
    hos_s_version =  models.CharField(max_length=255)
    hos_stock_version =  models.CharField(max_length=255)
    hos_ereferral_version =  models.CharField(max_length=255)
    date_created = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.hcode + ' : ' + self.app_controlVersion


class ServerBand(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class OperationSystem(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class ServerServiceStatus(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class database(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class WebServer(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class ProfileServer(models.Model):
    ServerBand = models.ForeignKey(ServerBand, null=True,on_delete= models.SET_NULL)
    OperationSystem  = models.ForeignKey(OperationSystem, null=True,on_delete= models.SET_NULL)
    ContactPhone = models.CharField(max_length=255,default='')
    FixIpAddress = models.CharField(max_length=255,default='')
    hospitals = models.ForeignKey(Hospitals, null=True, on_delete= models.SET_NULL)
    datetimeSendServer = models.DateTimeField(null=True, blank=True)
    # case = models.ForeignKey(Case, null=True,on_delete= models.SET_NULL)
    ServerServiceStatus = models.ForeignKey(ServerServiceStatus, null=True,on_delete= models.SET_NULL)
    Memo = models.CharField(max_length=255,default='')
    ContactFirstName = models.CharField(max_length=255,default='')
    ContactLastName = models.CharField(max_length=255,default='')
    ContactEmail = models.CharField(max_length=255,default='')
    datetimeReceiveServer = models.DateTimeField(null=True, blank=True)
    ServerImage = models.ImageField(blank=True)
    UseServer =  models.CharField(max_length=255,default='')
    dbBackup =  models.CharField(max_length=255,default='')
    database  = models.ForeignKey(database, null=True,on_delete= models.SET_NULL)
    webServer  = models.ForeignKey(WebServer, null=True,on_delete= models.SET_NULL)
    datetimeCompleteServer =  models.DateTimeField(null=True, blank=True)
    update_at =  models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.hospitals.label




# model5

class model5_lookup_error(models.Model):
    err_code = models.TextField()
    err_detail = models.TextField()

    def __str__(self):
        return self.err_code + ' : ' + self.err_detail



class model5_recap_report(models.Model):
    hcode = models.CharField(max_length=255)
    hname = models.CharField(max_length=255)
    req_claimcode = models.CharField(max_length=255)
    req_claim = models.CharField(max_length=255)
    approved = models.CharField(max_length=255)
    denined = models.CharField(max_length=255)
    dataknow = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.hcode + ' : ' + self.hname

class error_detail(models.Model):
    hcode = models.CharField(max_length=255)
    err_code = models.CharField(max_length=255)
    err_detail =  models.CharField(max_length=255)
    total_denined =  models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.hcode + ' : ' + self.err_detail

class datatimeperiod(models.Model):

    hcode = models.CharField(max_length=255)
    hname = models.CharField(max_length=255)
    over5day =  models.CharField(max_length=255)
    under5day  =  models.CharField(max_length=255)

    def __str__(self):
        return self.hcode + ' : ' + self.over5day