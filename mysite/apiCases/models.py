from django.db import models

# Create your models here.


class ApiAppNhsoBkk(models.Model):
    callback_id = models.CharField(max_length=255,null=True)
    callback_code = models.CharField(max_length=255,null=True)
    callback_title = models.CharField(max_length=255,null=True)
    callback_group_id = models.CharField(max_length=255,null=True)
    callback_subgroup_id = models.CharField(max_length=255,null=True)
    callback_tag = models.CharField(max_length=255,null=True)
    staff_id = models.CharField(max_length=255,null=True)
    profile = models.CharField(max_length=255,null=True)
    callback_name = models.CharField(max_length=255,null=True)
    mobile_phone = models.CharField(max_length=255,null=True)
    detail = models.CharField(max_length=255,null=True)
    insert_at = models.DateTimeField(auto_now_add=True, null=True)
    case_locking = models.CharField(max_length=7, default='0')
    case_lock_date_time = models.DateTimeField(null=True, blank=True)
    case_staff_lock = models.CharField(max_length=255,null=True)
    def __str__(self):
        return self.callback_code