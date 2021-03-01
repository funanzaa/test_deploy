
from django.db import models
from django.contrib.auth.models import User
from crm.models import ProfileServer,ServerServiceStatus

# Create your models here.

class versHosEreferral(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class versErefws(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class ProfileEreferral(models.Model):
    ProfileServer = models.ForeignKey(ProfileServer, null=True,on_delete= models.SET_NULL) # add
    ContactFirstName = models.CharField(max_length=255,null=True)
    ContactLastName = models.CharField(max_length=255,null=True)
    ContactPhone = models.CharField(max_length=255,null=True)
    request_at = models.DateTimeField(null=True, blank=True)
    success_at = models.DateTimeField(null=True, blank=True)
    update_at = models.DateTimeField(null=True, blank=True)
    ServerServiceStatus = models.ForeignKey(ServerServiceStatus, null=True,on_delete= models.SET_NULL) # add
    created_by = models.CharField(max_length=255,null=True)
    update_by =  models.CharField(max_length=255,null=True)
    versHosEreferral = models.ForeignKey(versHosEreferral, null=True,on_delete= models.SET_NULL) # add
    versErefws = models.ForeignKey(versErefws, null=True,on_delete= models.SET_NULL) # add
    EreferMemo = models.TextField(null=True)


