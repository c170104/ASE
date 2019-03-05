from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *



# Create your views here.

#Returns the home page for display (left the calendar to display)
@login_required
def home(request):
	events = Announcement.objects.all()
	events = events.extra(order_by = ['-eventDate'])
	return render(request, 'index.html', {'active_page': 'home', 'announcements' : events })


#This function is for the main page of scheduling, can be used by both teachers and parents (left the calendar to display)
@login_required
def schedule(request):
	return render(request, 'schedule/schedule.html', {'active_page': 'schedule'})

#This function is for the teachers to add new event that can be announcments/events (completed)
@login_required
def schedule_add(request, current='events'):
	event_categories = ('events', 'announcements')
	if current not in event_categories:
		#The warning below can be used for bootstrap to call messages which will display as a warning with the message
		messages.warning(request, f'Invalid path indicated to {current}!')
		#Redirects user to the add page to add new events if the parameters does not meet the tabs we have
		return redirect ('schedule-add')
	
	else:
		if current == event_categories[0]:
			form = EventForm(request.POST)
			if form.is_valid():
				event = form.save(commit=False)
				event.eventPlanner = EventPlanner.objects.get(user__exact = request.user.id)
				form.save()
				messages.success(request, f'Event has been created successfully!')
				return redirect('schedule-add')

		elif current == event_categories[1]:
			form = AnnouncementForm(request.POST)
			if form.is_valid():
				announcement = form.save(commit=False)
				announcement.creator = request.user.username
				form.save()
				messages.success(request, f'Announcement has been created successfully!')
				return redirect('schedule-add')
	
	return render(request, 'schedule/schedule_add.html', {'active_page': 'schedule', 'active_tab': current, 'form' : form})

#This function is used for displaying and managing schedules for teachers (Completed)
@login_required
def schedule_manage(request, current='confirmed'):
	event_types = ('confirmed', 'pending', 'announcements')
	if current not in event_types:
		#Redirects user to the manage page with the active tab being confirmed if the parameters does not meet the tabs we have
		return redirect ('schedule-manage')

	else:
		if current == event_types[0]:
			#Look for a planner that belongs to the current user and searches for all the events within it
			#get method will produce error if more than 1 planner is found.
			planner = EventPlanner.objects.get(user__exact = request.user.id)
			events = Event.objects.filter(eventPlanner__exact = planner)

		elif current == event_types[1]:
			#Look for a planner that belongs to the current user and searches for all the events within it
			#get method will produce error if more than 1 planner is found.
			planner = EventPlanner.objects.get(user__exact = request.user.id)
			events = Appointment.objects.filter(eventPlanner__exact = planner).values()
			#This replaces the parent_id with the name of the parent
			for event in events:
				event['parent_id'] = ParentProfile.objects.get(id__exact = event['parent_id'])
	
		elif current == event_types[2]:
			events = Announcement.objects.filter(creator__exact = request.user.username)

		return render(request, 'schedule/schedule_manage.html', {'active_page': 'schedule', 'active_tab': current, 
				'events': events })

