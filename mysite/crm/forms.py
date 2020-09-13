from django.forms import ModelForm
from django.core import validators
from django import forms
from .models import *


class CaseForm(ModelForm):
    hospitals = forms.ModelChoiceField(queryset=Hospitals.objects.order_by('label')) ## order in from
    class Meta():
        model = Case
        fields = ['name','project', 'project_subgroup','resolution','service','hospitals','case_pic','created_by']
        # fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['created_by'].initial = 1 # default created_by
            self.fields['name'].widget = forms.TextInput(attrs={"class":"form-control", 'required': False})
            self.fields['created_by'].widget = forms.HiddenInput()
            self.fields['name'].widget = forms.TextInput(attrs={"class":"form-control"})
            self.fields['project'].widget.attrs['class'] = 'form-control'
            self.fields['project_subgroup'].widget.attrs['class'] = 'form-control'
            self.fields['service'].widget.attrs['class'] = 'form-control'
            self.fields['hospitals'].widget.attrs['class'] = 'form-control'
            self.fields['resolution'].widget = forms.Textarea(attrs={"class":"form-control"})

class updateCaseForm(ModelForm):
    class Meta():
        model = Case
        fields = ['name','project', 'project_subgroup','resolution','service','hospitals','case_pic']
        # fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(updateCaseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['name'].widget = forms.TextInput(attrs={"class":"form-control"})
            self.fields['resolution'].widget = forms.Textarea(attrs={"class":"form-control"})


        
class hospitalForm(forms.Form):
    type_choice = (
        ("1", "โรงพยาบาล"),
        ("3", "ศูนย์บริการสาธารณสุข"),
        ("4", "คลินิก"),
    )

    code = forms.CharField( max_length=5,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'code'}))
    label = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Label'}))
    h_type = forms.ChoiceField(label="h_type", choices = type_choice, widget=forms.Select(attrs={"class":"form-control"}))


class editHospitalForm(forms.Form):
    type_choice = (
        ("1", "โรงพยาบาล"),
        ("3", "ศูนย์บริการสาธารณสุข"),
        ("4", "คลินิก"),
    )

    code = forms.CharField( max_length=5,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'code'}))
    label = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Label'}))
    h_type = forms.ChoiceField(label="h_type", choices = type_choice, widget=forms.Select(attrs={"class":"form-control"}))