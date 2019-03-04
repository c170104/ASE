from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ReportCardPage, SubjectGrade
from .forms import EventForm, AnnoucementForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'index.html', {'active_page': 'home'})


#This function is for the main page of scheduling, can be used by both teachers and parents
@login_required
def schedule(request):
	return render(request, 'schedule/schedule.html', {'active_page': 'schedule'})

#This function is for the teachers to add new event that can be announcments/events
@login_required
def schedule_add(request, current='events'):
	event_categories = ('events', 'announcements')
	if current not in event_categories:
		#The warning below can be used for bootstrap to call messages which will display as a warning with the message
		messages.warning(request, f'Invalid path indicated to {current}!')
		#Redirects user to the add page to add new events if the parameters does not meet the tabs we have
		return redirect ('schedule-add')
	
	elif current == event_categories[0]:
		form = EventForm(request.POST)

		#Create objects to add into classes!

	elif current == event_categories[1]:
		form = AnnoucementForm()
		#Create objects to add into classes!
	
	return render(request, 'schedule/schedule_add.html', {'active_page': 'schedule', 'active_tab': current, 'form' : form})

#This function is used for manage scheduling page
#@login_required
def schedule_manage(request, current='confirmed'):
	event_types = ('confirmed', 'pending', 'announcements')
	if current not in event_types:
		#The warning below can be used for bootstrap to call messages which will display as a warning with the message
		messages.warning(request, f'Invalid path indicated to {current}!')
		#Redirects user to the manage page with the active tab being confirmed if the parameters does not meet the tabs we have
		return redirect ('schedule-manage')

	else:
		#Pull the relevant data and return
		return render(request, 'schedule/schedule_manage.html', {'active_page': 'schedule', 'active_tab': current})


def event_delete(request, username, eventid):
	#Pull the data and return + process the form
	return render(request, 'events_delete.html', {'active_page': 'schedule'})

