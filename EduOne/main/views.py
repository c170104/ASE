from .decorators import staff_required, parent_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import staff_required, parent_required
from .models import *
from .forms import *
from .functions import *
import datetime
from datetime import timedelta
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

# #This function is used for displaying and managing schedules for teachers 
# @login_required
def schedule_manage(request, current='confirmed'):
	event_types = ('confirmed', 'pending', 'announcements')
	if current not in event_types:
		#Displays a forbidden error
		return HttpResponseForbidden()

	else:
		#Look for a planner that belongs to the current user and searches for all the events within it
		planner = EventPlanner.objects.get(user__exact = request.user.id)
		appointment = Appointment.objects.filter(eventPlanner__exact = planner)

		if current == event_types[0]:
			#get method will produce error if more than 1 planner is found.
			events = Event.objects.filter(eventPlanner__exact = planner).extra(order_by = ['-dateFrom'])


		elif current == event_types[1]:
			#get method will produce error if more than 1 planner is found.
			events = appointment.filter(apptStatus__exact = 'pending').extra(order_by = ['-apptDate']).values()
			#This replaces the parent_id with the name of the parent
			for event in events:
				event['parent_id'] = ParentProfile.objects.get(id__exact = event['parent_id'])	
	
		elif current == event_types[2]:
			events = Announcement.objects.filter(user__exact = request.user.id).extra(order_by = ['-dateCreated'])

		return render(request, 'schedule/schedule_manage.html', {'active_page': 'schedule', 'active_tab': current, 
				'events': events })

#function defines the approve and rejection tools for teachers (left rejection detials)
def schedule_pending_manage(request, pk=None, status=None):
	if(not pk or not status):
		#Displays a forbidden error
		return HttpResponseForbidden()
	else:
		status_list = ('approved', 'rejected')
		planner = EventPlanner.objects.get(user__exact = request.user.id)

		#If an appointment is approved, we update the status to approve
		if status == status_list[0]:
			events = Appointment.objects.filter(id__exact = pk)
			events.update(apptStatus = 'approved')

		#Create an event for the teacher with regards to the appointment
			for event in events:
				Event.objects.create(eventPlanner = planner, title = event.apptTitle, description = event.apptDescription,
					location = event.apptLocation, dateFrom = event.apptDate, dateTo = event.apptDate, timeFrom = event.apptTimeFrom, timeTo = event.apptTimeTo)

			messages.success(request, f'Appointment has been approved!')
			return redirect('schedule-manage')
		
		elif status == status_list[1]:
			try:
				'''
				Rejection try to come up with form to enter rejection details using POST
				'''

			except ObjectDoesNotExist:
				print("Appointment does not exist!")	

		return render(request, 'schedule/schedule_appointment_edit.html', {'form':form})
		

######################### Lawrann #########################
@login_required
def childlist(request):
	if request.user.is_staff: 
		return HttpResponseForbidden()
	current_user = request.user
	parentid = current_user.id
	childstudent = Student.objects.all()
	CHILDLIST = []
	for i in childstudent:
		if i.child_of.user.id == parentid:
			CHILDLIST.append(i)
	context = {
		'CHILDLIST' : CHILDLIST,
		'active_page': 'childprofile'
	}
	return render(request, 'child/childlist.html', context)

@login_required
def childprofile(request, id=None):
	if request.user.is_staff: 
		return HttpResponseForbidden()
	childStudent = Student.objects.get(nric = id)
	if childStudent.child_of.user.id != request.user.id:
		return HttpResponseForbidden()
	reportCard = ReportCard.objects.get(student__exact = childStudent)
	REPORTCARDLIST = []
	rcp = ReportCardPage.objects.all()
	# print(rcp)
	for i in rcp:
		if i.reportCard.id == reportCard.id:
			REPORTCARDLIST.append(i)
	REPORTCARDLIST.sort(key=lambda r: r.exam_date, reverse = True)

	attendance = Attendance.objects.filter(student=childStudent)
	ATTENDANCELIST = []
	for i in attendance:
		ATTENDANCELIST.append(i)
	ATTENDANCELIST.sort(key=lambda r: r.date, reverse = True)
	# ATTENDANCELISTSLICED = ATTENDANCELIST[0:7]
	WEEKLIST = [] # stores the current week monday to sunday
	now = datetime.datetime.now() # get todays date
	print(now.weekday()) # monday : 0 sunday : 6
	print(now.date())
	WEEKLIST.append(now.date())
	toSun = 6-int(now.weekday()) # how many extra days to sunday
	forMon = int(now.weekday())
	for i in range(forMon):
		print(i)
		WEEKLIST.append(now.date()-timedelta(days=i+1))
	for i in range(toSun):
		WEEKLIST.append(now.date()+timedelta(days=i+1))
	WEEKLIST.sort()
	DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	# print(WEEKLIST)
	# for i in range(toSun):
	# 	WEEKLIST.append((now.weekday()+i+1,now.date()+timedelta(days=1))


	# for i in range(forMon):
	# 	WEEKLIST.append((forMon-i,now.date()-timedelta(days=i))
    # 	print()

	comment = Comment.objects.filter(student=childStudent).order_by("commentDate")
	COMMENTLIST = []
	for i in comment:
		COMMENTLIST.append(i)
	COMMENTLISTSLICED = COMMENTLIST[0:3]
	
	# print(COMMENTLISTSLICED)

	context = {
		'childStudent' : childStudent,
		'reportCard' : reportCard,
		'REPORTCARDLIST' : REPORTCARDLIST,
		'ATTENDANCELIST' : ATTENDANCELIST,
		'WEEKLIST' : WEEKLIST,
		'DAYS':DAYS,
		# 'ATTENDANCELISTSLICED' : ATTENDANCELISTSLICED,
		'COMMENTLIST' : COMMENTLIST,
		'COMMENTLISTSLICED' : COMMENTLISTSLICED,
	}
	return render(request, 'child/child-profile.html', context)

@login_required
def childreportcardpage(request, id=None, rcid=None):
	student = Student.objects.get(nric__exact = id)
	reportcard = ReportCard.objects.get(student__exact = student)
	reportcardpage = ReportCardPage.objects.get(reportCard__exact = reportcard, id__exact = rcid)
	SUBJECTGRADELIST = []
	subjectgrade = SubjectGrade.objects.filter(reportCardPage__exact = reportcardpage)
	for i in subjectgrade:
		SUBJECTGRADELIST.append(i)
	# print(SUBJECTGRADELIST)
	context = {
		'student' : student,
		'reportcardpage' : reportcardpage,
		'SUBJECTGRADELIST' : SUBJECTGRADELIST,
	}
	return render(request, 'child/child-report-card-page.html', context)

@login_required
def childattendance(request, id=None):
	student = Student.objects.get(nric__exact = id)
	attendance = Attendance.objects.filter(student=student)
	ATTENDANCELIST = []
	for i in attendance:
		ATTENDANCELIST.append(i)
	ATTENDANCELIST.sort(key=lambda r: r.date, reverse = True)
	context = {
		'ATTENDANCELIST':ATTENDANCELIST
	}
	return render(request, 'child/child-attendance.html', context)

@login_required
def childcomments(request, id=None):
	student = Student.objects.get(nric__exact = id)
	comment = Comment.objects.filter(student=student).order_by("commentDate")
	COMMENTLIST = []
	for i in comment:
		COMMENTLIST.append(i)
	context = {
		'COMMENTLIST':COMMENTLIST
	}
	return render(request, 'child/child-comments.html', context)

@login_required
def appointment_add(request):
	if request.user.is_staff: 
		return HttpResponseForbidden()
	current_user = request.user
	CHILDOFPARENTS = [] ## CHILDOFPARENTS stores the child object associated with the parent
	FORMCLASS = [] ## FORMCLASS stores the formclass of the parent's child
	STAFFCHOICES = [] ## STAFFCHOICES stores the (eventplanner, Staff firstname lastname)
	## getting the parentid of request.user
	childstudent = Student.objects.all()
	for i in ParentProfile.objects.all():
			if i.user.id == request.user.id:
				parentid = i.user.id
				break
	## getting the children/s associated with the parentid && the formclass associated with the children
	for i in childstudent:
		if i.child_of.user.id == parentid:
			CHILDOFPARENTS.append(i)
			FORMCLASS.append(i.form_class)
	## getting the Staff associated with each form class
	for i in FORMCLASS:
		# STAFFCHOICES.append(StaffProfile.objects.get(form_class = i.id))
		staff = StaffProfile.objects.get(form_class = i.id)
		staffn = staff.firstname + ' ' + staff.lastname 
		staffuid = staff.user.id
		eventP = EventPlanner.objects.get(user = staffuid)
		# print(eventP)
		# print(staffn)
		STAFFCHOICES.append((eventP,staffn))
	STAFFCHOICES.append(('none','none'))
	form = AppointmentForm(request.POST, stafflist = STAFFCHOICES)


	if form.is_valid():
		appointment = form.save(commit=False)
		staffname = form.cleaned_data['stafflist'] # Pull the selected name form choicefield
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
			try:
				event = Event.objects.get(id__exact = pk)
				user_id = EventPlanner.objects.get(id__exact = event.eventPlanner_id).user_id
				next_path = 'confirmed'
				form = EventForm(request.POST or None, instance=event)
			except ObjectDoesNotExist:
				print("No entries found for schedule_edit!")	

		elif stype == schedule_types[1] and pk:
			try:
				event = Appointment.objects.get(id__exact = pk)
				user_id = EventPlanner.objects.get(id__exact = event.eventPlanner_id).user_id
			except ObjectDoesNotExist:
				print("No entries found for schedule_edit!")	

		elif stype == schedule_types[2] and pk:	
			try:
				event = Announcement.objects.get(id__exact = pk)
				user_id = event.user_id
				next_path = 'announcements'
				form = AnnouncementForm(request.POST or None, instance=event)
			except ObjectDoesNotExist:
				print("No entries found for schedule_edit!")	

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
	try:
		information = {}
		present = []
		information['attendanceCount'] = 0
		information['today'] = date
		information['teacher_info'] = StaffProfile.objects.get(user__exact = request.user.id)
		information['students'] = Student.objects.filter(form_class__exact = information['teacher_info'].form_class)
		for student in information['students']:
			
				student = Attendance.objects.get(student__exact = student, date__exact = date).student
				present.append(student)
				information['attendanceCount'] = information['attendanceCount'] + 1

	except ObjectDoesNotExist:
				print("No entries found for attendance!")

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

#This function defines the subject classes that a teacher teach and is able to comment on the student
def performance(request, class_id=None):
	information = {}
	information['subjects'] = {}
	information['view'] = 'subject'
	information['teacher_info'] = StaffProfile.objects.get(user__exact = request.user.id)
	subject_objects = SubjectClass.objects.filter(teacher_id__exact = information['teacher_info'].id)


	#Filters any duplicates in the class from multiple subjects
	subject_class_objects = []
	for sclass in subject_objects:
		if sclass.classOf not in subject_class_objects:
			subject_class_objects.append(sclass.classOf)	
	#Saves the information inside a list
	information['subject_classes'] = subject_class_objects
	

	#If a class is specified, then display all the subjects taught within that class
	if class_id:
		subject_names = []
		for subject in subject_objects:
			if subject.classOf_id == class_id:
				subject_names.append(subject.subject)
		
		information['subjects'] = subject_names		

	try:
		subject_types = ('English', 'Maths', 'Science', 'Chinese') #These subjects should pull from a database in the future
		if (request.GET['subject_chosen']):
			information['view'] = 'students'
			subject_chosen = request.GET['subject_chosen']
			if subject_chosen not in subject_types:
				return HttpResponseForbidden()

			else:
				for subject_class in subject_objects:
					if (subject_class.classOf_id == class_id):
						information['class_name'] = Class.objects.get(id__exact = subject_class.classOf_id)
						if (subject_class.subject == subject_chosen):
							students_in_subject = StudentToSubjectClass.objects.filter(subjectClass_id__exact = subject_class.id).values()

				student_list = []		
				for stud in students_in_subject:
					student_list.append(Student.objects.get(nric__exact = stud['student_id']))
					

				information['students'] = student_list
				information['subject_chosen'] = subject_chosen
				information['class_id'] = class_id
				
	except:
		pass		
	
	return render(request, 'student_settings/performance.html',{'active_page': 'student', 'information': information})	

#This function is used to add new comments for students under a class and subject
def comment_add(request, class_id, subject, id):
	if (not class_id or not subject or not id):
		return HttpResponseForbidden()
	
	else:
		try:
			information = {}
			information['student'] = Student.objects.get(nric__exact = id)
			form = CommentForm(request.POST)
			if form.is_valid():
				comment = form.save(commit=False)
				comment.student = information['student'] 
				comment.commentBy = request.user
				comment.commentDate = datetime.datetime.now().date()
				comment.commentTime = datetime.datetime.now().strftime("%H:%M:%S")				
				form.save()
				messages.success(request, f'Comment for student has been submitted successfully!')
				return redirect('performance-home')

		except ObjectDoesNotExist:
				print("No entries found for comment_add!")
				messages.failure(request, f'Something went wrong when trying to comment!')
				return redirect('performance-home')		

	
	return render(request, 'student_settings/performance_add.html',{'active_page': 'student', 'information': information, 'form' : form})	

#This function displays the students from the teacher's form class
def grades(request, id=None):
	try:
		information = {}
		information['teacher_info'] = StaffProfile.objects.get(user__exact = request.user.id)
		information['students'] = Student.objects.filter(form_class__exact = information['teacher_info'].form_class).values()
		information['view'] = 'class'

		if (id != None):
			information['view'] = 'student'
			student = Student.objects.get(nric__exact = id)
			report_card = ReportCard.objects.get(student = student)
			information['nric'] = id
			information['pages'] = ReportCardPage.objects.filter(reportCard__exact = report_card)

	except ObjectDoesNotExist:
				print("No entries found for grades!")
					
	return render(request, 'student_settings/grades.html', {'active_page': 'student', 'information': information})

#This function displays the list of report card pages
def grades_manage(request, report_card_page_id=None, id=None):
	if (not id or not report_card_page_id):
		return HttpResponseForbidden()

	try:
		information = {}
		page = ReportCardPage.objects.get(id__exact = report_card_page_id)
		report_card = ReportCard.objects.get(id__exact = page.reportCard_id)
		if report_card.student_id == id:
			 information['grades'] = SubjectGrade.objects.filter(reportCardPage_id__exact = report_card_page_id)
			 information['report_card'] = page
			 information['nric'] = id
		else:
			 return HttpResponseForbidden()	 


	except ObjectDoesNotExist:
				print("No entries found for report card pages!")		

	return render(request, 'student_settings/grades_manage.html', {'active_page': 'student', 'information': information})			

#NOT FINSIHED!
def grades_add(request, id=None):
	if (not id):
		return HttpResponseForbidden()

	try:
		form = SubjectGradeForm(request.POST or None)
		if form.is_valid():
			print('YAY')

		return render(request, 'student_settings/grades_add.html', {'active_page': 'student', 'form':form})				

	except ObjectDoesNotExist:
				print("No entries found for report card pages!")		

			