from django.conf.urls import url
from first_app import views

# app_name = 'first_app'

urlpatterns = [
    url(r'^$',views.level_1, name='level_1'),
    url(r'^users/',views.users, name='users'),
    url(r'^form/',views.form_name_view, name='form_name_view'),
    url(r'^add_users/',views.add_users, name='add_users'),
    url(r'^relative_url/$',views.relative_url, name= 'relative_url'),
    url(r'^register/',views.register, name= 'register'),
    url(r'^login/$',views.user_login, name= 'user_login')
]
