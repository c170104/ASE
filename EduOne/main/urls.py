"""EduOne URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, forms
from .forms import *


urlpatterns = [
###==================================Common===========================================================    

    ##Start of paths for login & logout
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    #End of paths for login & logout

    ##(Common) Start of main path for the website
    path('home/', views.home, name='main-home'),
    #End of main path for the website

    ##(Common) Start of common paths for scheduling functions 
    path('schedule/', views.schedule, name='schedule-home' ),
    path('schedule/<int:month>/<int:year>', views.schedule, name='schedule-home' ),
    #End of common paths for scheduling functions (parents & teachers)

###==================================End of Common=========================================================== 

###==================================Teachers Functions=========================================================== 
    ##(Teachers) Start of scheduling functions for teachers
    path('schedule/manage/', views.schedule_manage, name='schedule-manage'),
    path('schedule/manage=<str:current>/', views.schedule_manage, name='schedule-manage'),
    path('schedule/add/', views.schedule_add, name='schedule-add'),
    path('schedule/add=<str:current>/', views.schedule_add, name='schedule-add'),
    path('schedule/edit=<str:stype>/<int:pk>/', views.schedule_edit, name='schedule-edit'), 
    #End of paths for scheduling functions

    #(Teachers) Start of django class form for scheduling functions
    path('announcement/<int:pk>/', AnnouncementDetailView.as_view(), name = 'announcement-detail'),
    path('announcement/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name = 'announcement-delete'),
    path('event/<int:pk>/', EventDetailView.as_view(), name = 'event-detail'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name = 'event-delete'),
    path('appointment/<int:pk>/', AppointmentDetailView.as_view(), name = 'appointment-detail'),
    #End of django class form for scheduling functions

    #(Teachers) Start of paths for student settings functions
    path('attendance/', views.attendance, name='attendance-home' ),
    path('grades/', views.grades, name='grades-home' ),
    #End of paths for student settings functions

###===========================End of Teachers Functions=========================================================== 

###==================================Parents Functions=========================================================== 

    ##(Parents) Start of paths for parent's scheduling functions
    path('schedule/appointment-add/', views.appointment_add, name='appointment-add'), 
    path('appointment-pending/<int:pk>/delete/', AppointmentPendingDeleteView.as_view(template_name = "appointment/appointment_pending_delete.html"), name = 'appointment-pending-delete'),
    path('appointment-approved/<int:pk>/delete/', AppointmentApprovedDeleteView.as_view(template_name = "appointment/appointment_approved_delete.html"), name = 'appointment-approved-delete'),
    #End of paths for parent's scheduling functions

    ##(Parents) Start of django class form for scheduling functions
    path('appointment-edit/<int:pk>/delete/', views.AppointmentUpdate.as_view(template_name = "appointment/appointment_update.html"), name = 'appointment-update'),
    #End of django class form for scheduling functions

###===========================End of Parents Functions===========================================================     

###=========================== For Trials======================================================

]
