# """EduOne URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/2.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

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
    # End of common paths for scheduling functions (parents & teachers)

###==================================End of Common=========================================================== 

###==================================Teachers Functions=========================================================== 
    ##(Teachers) Start of scheduling functions for teachers
    path('schedule/manage/', views.schedule_manage, name='schedule-manage'),
    path('schedule/manage=<str:current>/', views.schedule_manage, name='schedule-manage'),
    path('schedule/<str:status>/<int:pk>', views.schedule_pending_manage, name='schedule-pending-manage'),
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
    #End of paths for scheduling functions

    #(Teachers) Start of paths for student settings functions
    path('attendance/', views.attendance, name='attendance-home'),
    path('attendance/<str:status>/<str:id>', views.attendance_edit, name='attendance-edit' ),

    path('grades/', views.grades, name='grades-home' ), #Student Settings -> Manage Grades
    path('grades/<str:id>', views.grades, name='grades-home'), #Student Settings -> Manage Grades -> Manage Grades
    path('grades/<str:id>/<int:report_card_page_id>', views.grades_manage, name='grades-manage'), #Student Settings -> Manage Grades -> Manage Grades -> Click examination name
    path('grades/<str:id>/<int:report_card_page_id>/add/', views.grades_add, name='grades-add' ), #not finished
    path('grades/<str:id>/<int:report_card_page_id>/edit/<int:pk>', grades_edit.as_view(template_name = "student_settings/grades_edit.html"), name='grades-edit'), #Student Settings -> Manage Grades -> Manage Grades -> Click examination name -> Click edit

    path('grades/<str:id>/add/<int:count>', views.report_card_page_add, name='report-card-page-add' ), #not finished


    path('performance/', views.performance, name='performance-home'),
    path('performance/<int:class_id>', views.performance, name='performance-home'),
    path('performance/<int:class_id>/<str:subject>/<str:id>', views.comment_add, name='performance-add'),
    #End of paths for student settings functions
###===========================End of Teachers Functions=========================================================== 

###==================================Parents Functions=========================================================== 
    #Start of paths for parent's scheduling functions
    path('schedule/appointment-add/', views.appointment_add, name='appointment-add'), 
    path('schedule/appointment-manage/', views.appointment_manage, name='appointment-manage'),
    path('schedule/appointment-manage=<str:current>/', views.appointment_manage, name='appointment-manage'),
    #End of paths for parent's scheduling functions
    
    #Start of paths for appointment's manage functions
    path('appointment-edit/<int:pk>/', AppointmentUpdate.as_view(template_name = "appointment/appointment_update.html"), name = 'appointment-update'),
    path('appointment-pending/<int:pk>/delete/', AppointmentPendingDeleteView.as_view(template_name = "appointment/appointment_pending_delete.html"), name = 'appointment-pending-delete'),
    path('appointment-approved/<int:pk>/delete/', AppointmentApprovedDeleteView.as_view(template_name = "appointment/appointment_approved_delete.html"), name = 'appointment-approved-delete'),
    #End of paths for appointment's manage functions\

    #Start of paths for child's profile functions
    path('childslist/', views.childlist, name='childs'),
    path('childslist/<str:id>/profile/', views.childprofile, name='child-profile'),
    path('childslist/<str:id>/profile/reportcard/<int:rcid>/', views.childreportcardpage, name='report-card-page'),
    path('childslist/<str:id>/profile/reportcard/<int:pk>/acknowledge', ReportCardPageAcknowledgementView.as_view(template_name = "child/child-report-card-acknowledge.html"), name='report-card-page-acknowledge'),
    path('childslist/<str:id>/profile/attendance/', views.childattendance, name='child-attendance'),
    path('childslist/<str:id>/profile/comments/', views.childcomments, name='child-comments'),
    #End of paths for child's profile functions
###===========================End of Parents Functions===========================================================     

###=========================== For Trials======================================================

]
