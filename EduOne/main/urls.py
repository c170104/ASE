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

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('home/', views.home, name='main-home'),
    path('schedule/', views.schedule, name='schedule-home' ),
    path('schedule/add/', views.schedule_add, name='schedule-add'),
    path('schedule/add=<slug:current>/', views.schedule_add, name='schedule-add'),
    path('schedule/manage/', views.schedule_manage, name='schedule-manage'),
    path('schedule/manage=<slug:current>/', views.schedule_manage, name='schedule-manage'),
    path('schedule/manage/delete', views.event_delete, name='event-delete'),
]
