from .decorators import staff_required, parent_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import staff_required, parent_required
from .models import *
from .forms import *
from .functions import *
import datetime
from django.views.generic import UpdateView
from django.urls import reverse_lazy

# # Create your views here.
# #Returns the home page for display (left the calendar to display)
# @login_required
def home(request, month=datetime.datetime.now().month, year=datetime.datetime.now().year):
	events = Announcement.objects.all().extra(order_by = ['-dateCreated'])
	planner = EventPlanner.objects.get(user__exact = request.user.id)
	calendar = getCalendarInformation(planner, month, year)

	return render(request, 'index.html', {'active_page': 'home', 'announcements' : events, 'calendar': calendar})


# #This function is for the main page of scheduling, can be used by both teachers and parents (left the calendar to display)
# @login_required
def schedule(request, month=datetime.datetime.now().month, year=datetime.datetime.now().year):
	planner = EventPlanner.objects.get(user__exact = request.user.id)
	calendar = getCalendarInformation(planner, month, year)
		
	return render(request, 'schedule/schedule.html', {'active_page': 'schedule', 'calendar': calendar})

# #This function is for the teachers to add new event that can be announcments/events (completed)
# @login_required
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
				announcement.user_id = request.user.id
				announcement.dateCreated = datetime.datetime.now().date()
				form.save()
				messages.success(request, f'Announcement has been created successfully!')
				return redirect('schedule-add')
	
	return render(request, 'schedule/schedule_add.html', {'active_page': 'schedule', 'active_tab': current, 'form' : form})

# #This function is used for displaying and managing schedules for teachers (Left Appointments Approve/Reject Portion)
# @login_required
def schedule_manage(request, current='confirmed'):
	event_types = ('confirmed', 'pending', 'announcements')
	if current not in event_types:
		#Displays a forbidden error
		return HttpResponseForbidden()

	else:
		if current == event_types[0]:
			#Look for a planner that belongs to the current user and searches for all the events within it
			#get method will produce error if more than 1 planner is found.
			planner = EventPlanner.objects.get(user__exact = request.user.id)
			events = Event.objects.filter(eventPlanner__exact = planner).extra(order_by = ['-dateFrom'])
			
		elif current == event_types[1]:
			#Look for a planner that belongs to the current user and searches for all the events within it
			#get method will produce error if more than 1 planner is found.
			planner = EventPlanner.objects.get(user__exact = request.user.id)
			events = Appointment.objects.filter(eventPlanner__exact = planner).extra(order_by = ['-apptDate']).values()
			#This replaces the parent_id with the name of the parent
			for event in events:
				event['parent_id'] = ParentProfile.objects.get(id__exact = event['parent_id'])
	
		elif current == event_types[2]:
			events = Announcement.objects.filter(user__exact = request.user.id).extra(order_by = ['-dateCreated'])

		return render(request, 'schedule/schedule_manage.html', {'active_page': 'schedule', 'active_tab': current, 
				'events': events })

######################### Lawrann #########################
@login_required
def appointment_add(request):
	form = AppointmentForm(request.POST)
	if request.user.is_staff: 
		return HttpResponseForbidden()
	if form.is_valid():
		appointment = form.save(commit=False)
		staffname = form.cleaned_data['staffchosen'] # Pull the selected name form choicefield
		for i in EventPlanner.objects.all():
			if str(i) == staffname:
				appointment.eventPlanner = i
				appointment.eventPlanner.id = i.id
				break
		for i in ParentProfile.objects.all():
			if i.user == request.user:
				appointment.parent = i
				break
		appointment.apptStatus = 'pending'
		form.save()
		messages.success(request, f'Appointment has been created successfully!')
		return redirect('appointment-add')
	context = {
		'form':form
	}
	
	return render(request, 'appointment/appointment_add.html', context)

# @login_required
def appointment_manage(request, current='pending'):
	if request.user.is_staff: 
		return HttpResponseForbidden()
	event_types = ('approved', 'rejected', 'pending')
	current_user = request.user
	obj = list()
	sp = StaffProfile.objects.all()
	#OG code
	if current not in event_types:
		return redirect('appointment-manage')
	elif current == event_types[0]: #accepted
		for i in Appointment.objects.all():
			if i.parent.user == current_user and i.apptStatus == 'approved':
				obj.append(i)
	elif current == event_types[1]: #rejected
		for i in Appointment.objects.all():
			if i.parent.user == current_user and i.apptStatus == 'rejected':
				obj.append(i)
	elif current == event_types[2]: #pending
		for i in Appointment.objects.all():
			if i.parent.user == current_user and i.apptStatus == 'pending':
				obj.append(i)
	context = {
		'user' : current_user,
		'obj': obj,
		'staffprofilelist': sp,
		'active_page': current #approved rejected pending
		## 'location'
	}
	return render(request, 'appointment/appointment_manage.html', context)


# class AppointmentUpdate(LoginRequiredMixin,UpdateView):
#     model = Appointment
#     success_url = reverse_lazy('appointment-manage')
#     fields = [
# 		'apptTitle',
# 		'apptDescription',
# 		'apptDate',
# 		'apptLocation',
# 		'apptTimeFrom',
# 		'apptTimeTo'
# 	]

######################### Lawrann #########################
    
# #This function is used to edit scheduling information based on known forms (Left Appointments)
# @login_required
def schedule_edit(request, stype=None, pk=None):
	schedule_types = ('event', 'appointment', 'announcement')
	if stype not in schedule_types:
		#Displays a forbidden error
		return HttpResponseForbidden()

	else:
		#Get the different objects based on the schedule type
		if stype == schedule_types[0] and pk:
			event = Event.objects.get(id__exact = pk)
			user_id = EventPlanner.objects.get(id__exact = event.eventPlanner_id).user_id
			next_path = 'confirmed'
			form = EventForm(request.POST or None, instance=event)

		elif stype == schedule_types[1] and pk:
			event = Appointment.objects.get(id__exact = pk)
			user_id = EventPlanner.objects.get(id__exact = event.eventPlanner_id).user_id

		elif stype == schedule_types[2] and pk:	
			event = Announcement.objects.get(id__exact = pk)
			user_id = event.user_id
			next_path = 'announcements'
			form = AnnouncementForm(request.POST or None, instance=event)

		#Checks if the user has permissions to modify the contents	
		if request.user.id != user_id:
			return HttpResponseForbidden()

		else:
			if form.is_valid():
				form.save()
				messages.success(request, f'Modifications has been made successfully!')
				return redirect('schedule-manage', current=next_path)

		return render(request, 'schedule/schedule_edit.html', {'edit_type' : stype, 'form' : form, 'path':next_path })

# #This function is the main page for attendance taking (Uncompleted, left with updating attendance)
# @staff_required
def attendance(request, date = datetime.datetime.now()):
	information = {}
	present = []
	information['attendanceCount'] = 0
	information['today'] = date
	information['teacher_info'] = StaffProfile.objects.get(user__exact = request.user.id)
	information['students'] = Student.objects.filter(form_class__exact = information['teacher_info'].form_class)
	for student in information['students']:
		try:
			student = Attendance.objects.get(student__exact = student, date__exact = date).student
			present.append(student)
			information['attendanceCount'] = information['attendanceCount'] + 1

		except:
			pass

	information['present'] = present
	return render(request, 'student_settings/attendance.html', {'active_page': 'student', 'information': information})

#This function defines whether to add / remove students from the attendance list of that current day
def attendance_edit(request, id=None, status=None):
	status_types = ('Y', 'y', 'N', 'n', 'all', 'ALL')
	if status not in status_types:
		#Displays a forbidden error
		return HttpResponseForbidden()

	else:
		#Depends on the whether the student is present
		#If the student is present, this will delete the current record from the database in Attendance
		if (status == status_types[0] or status == status_types[1]) and id:
			student = Student.objects.get(nric__exact = id)
			try:
				student = Attendance.objects.get(student = student)
				student.delete()
			except Attendance.DoesNotExist:	
				student = None

		#If the student is not present, this will add the current record into the database in Attendance
		elif (status == status_types[2] or status == status_types[3]) and id:
			student = Student.objects.get(nric__exact = id)
			try:
				student = Attendance.objects.get(student = student)
			except Attendance.DoesNotExist:	
				Attendance.objects.create(student = student, date = datetime.datetime.now())
		
		#Adds the all students of the form class as present into the database in Attendance  
		elif (status == status_types[4]) and id:
			staff = StaffProfile.objects.get(user__exact = request.user.id)
			students = Student.objects.filter(form_class__exact = staff.form_class)
			for student in students:
				try:
					student = Attendance.objects.get(student = student)
				except Attendance.DoesNotExist:	
					Attendance.objects.create(student = student, date = datetime.datetime.now())

		return redirect('attendance-home')

	return render(request)


def grades(request):
	information = {}
	information['teacher_info'] = StaffProfile.objects.get(user__exact = request.user.id)
	information['students'] = Student.objects.filter(form_class__exact = information['teacher_info'].form_class)
	return render(request, 'student_settings/grades.html', {'active_page': 'student', 'information': information})

def performance(request):


	return render(request, 'student_settings/performance.html')	

