from rest_framework import serializers
from .models import *

class ControlVersionSerializer(serializers.ModelSerializer):  # ModelSerializer not link in url id
    app_controlVersion = serializers.CharField(required=False)
    hos_s_version = serializers.CharField(required=False)
    hos_stock_version = serializers.CharField(required=False)
    hos_ereferral_version = serializers.CharField(required=False)
    date_created =  serializers.DateTimeField(required=False)
    class Meta:
        model = ControlVersion
        # fields = (
        #     'h_type',
        #     'label',
        #     'code',
        #     'date_created'
        # )
        fields = '__all__'

class subProjectSerializer(serializers.ModelSerializer):  # ModelSerializer not link in url id
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    project = serializers.CharField(required=False)
    
    class Meta:
        model = Project_subgroup
        fields = (
            'id',
            'name',
            'project'
        )
