import django_filters

from .models import *

class caseFilter(django_filters.FilterSet):

    class Meta:
        model = Case
        fields = [
            'project',
            'project_subgroup',
            'service',
            'hospitals',
        ]
