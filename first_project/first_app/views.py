from django.shortcuts import render
from django.contrib.auth.models import User
from first_app.models import Topic,Webpage,AccessRecord
from . import forms
# from first_app.form_model import NewUserForm # add form
from first_app.form_user_model import UserForm, UserProfileInform # add form

# Login step 2

from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

#####

def index(request):
    context_dict = {'txt' : "hello world", 'number':100 }
    # helpdict = {'help_insert':'HELP PAGE'}
    return render(request,'first_app/home.html',context_dict)

def level_1(request):
    webpages_list = AccessRecord.objects.order_by('date')
    date_dict = {'access_records':webpages_list}
    return render(request,'first_app/level_1.html',context=date_dict)

def users(request):
    user_list = user_s.objects.all()
    print(user_list)
    user_dict = {'person':user_list}
    # return render(request,'first_app/users.html', context=user_dict)

def form_name_view(request):
    form = forms.FormName()
    if request.method == 'POST':
        form = forms.FormName(request.POST)
        if form.is_valid():
            # Do Something Code
            print(" VALIDATION SUCCESS!")
            print( "Name: " + form.cleaned_data['name'])
            print( "Email: " + form.cleaned_data['email'])
            print( "Text: " + form.cleaned_data['text'])
    return render(request,'first_app/form_page.html',{'form':form})

def add_users(request):

    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("Error Form Invalid")


    return render(request,'first_app/add_users.html',{'form':form})
#     return render(request,'first_app/add_users.html')


def relative_url(request):

    return render(request,'first_app/test_relative_url.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInform(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInform()

    return render(request,'registration/registration.html', {'user_form':user_form, 'profile_form': profile_form, 'registered': registered} )

# Login

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active")

        else:
            print("Someone tried to login and failed")
            print("Username:{} and Password: {}".format(username,password))
            return HttpResponse("Invalid login detail supplied")
    else:
        return render(request,'first_app/login.html',{})


# Logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in , Nice")
