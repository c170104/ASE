from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ReportCardPage, SubjectGrade

# Create your views here.
def home(request):
    return render(request, 'index.html', {'active_page': 'home'})



#@login_required
def schedule(request):
	return render(request, 'schedule.html', {'active_page': 'schedule'})



def schedule_add(request):
	return render(request, 'schedule.html', {'active_page': 'schedule'})


def schedule_manage(request, current='confirmed'):
	if current == 'pending':
		#Pull the list of appointments awaiting approval
		return render(request, 'schedule_manage.html', {'active_page': 'schedule', 'active_tab': current})

	elif current == 'announcements':
		#Pull the list of announcements available
		return render(request, 'schedule_manage.html', {'active_page': 'schedule', 'active_tab': current})

	else:
		return render(request, 'schedule_manage.html', {'active_page': 'schedule', 'active_tab': current})

