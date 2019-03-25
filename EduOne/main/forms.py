from django import forms
from django.forms import ModelForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Event, Announcement, EventPlanner, Appointment, StaffProfile, Comment, SubjectClass, SubjectGrade, ReportCardPage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
import decimal
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

# Do not use this form for user creation.
class UserCreationForm(ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Override base UserAdmin form for admin panel
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_parent')}
        ),
    )

# #This form is used by the views.schedule_add to add create new Event objects
class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['eventPlanner']
        labels = {
            'title': ('Event Title'),
            'description': ('Event Description'),
            'location': ('Location of Event'),
            'dateFrom': ('Start Date of Event'),
            'dateTo': ('End Date of Event'),
            'timeFrom': ('Start Time of Event'),
            'timeTo': ('End Time of Event'),
        }
        help_texts = {
            'title':('The title of the event goes here.'),
            'description' : ('The details of the event goes here.'),
            'location': ('The location details of event goes here.'),
            'dateFrom': ('The start date of the event goes here.'),
            'dateTo': ('The end date of the event goes here.'),
            'timeFrom' : ('The start time of the event goes here.'),
            'timeTo' : ('The end time of the event goes here.'),
        }


# #This form is used by the views.schedule_add to add create new Announcement objects
class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        exclude = ['user', 'dateCreated']
        labels = {
            'title' : ('Announcement Title'),
            'description': ('Announcement Description'),
        }
        help_texts = {
            'title' : ('The announcement title goes here.'),
            'description': ('The announcement description goes here.'),
        }


# # Do not use this form for user creation.
# class UserCreationForm(ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = '__all__'

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

# # Override base UserAdmin form for admin panel
# class UserAdmin(BaseUserAdmin):
#     add_form = UserCreationForm
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'is_staff', 'is_parent')}
#         ),
#     )

# #This class form is used by event-detail to view event details
class EventDetailView(DetailView):
    model=Event
    template_name = "schedule/event_detail.html"

# #This class form is used by announcement-detail to view event details
class AnnouncementDetailView(DetailView):
    model=Announcement
    template_name = "schedule/announcement_detail.html"

# #This class form is used by appointment-detail to view event details
class AppointmentDetailView(DetailView):
    model=Appointment      
    template_name = "schedule/appointment_detail.html" 

# #This class form is used by announcement-delete to delete existing announcements
class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = "schedule/announcement_confirm_delete.html"
    success_url = "/schedule/manage=announcements/"
    
    def test_func(self):
        announcement = self.get_object()
        if self.request.user == announcement.user:
            return True
        return False    

# #This class form is used by event-delete to delete existing events
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "schedule/event_confirm_delete.html"
    success_url = "/schedule/manage=confirmed/"
    
    def test_func(self):
        event = self.get_object()
        user_id = EventPlanner.objects.get(id__exact = event.eventPlanner_id).user_id
        if self.request.user.id == user_id:
            return True
        return False         

<<<<<<< HEAD
class grades_edit(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = SubjectGrade
    success_url = reverse_lazy('grades-home')
    fields = [
        'marks',
    ]
    def test_func(self):
        return True

class Grades_Add_Form(ModelForm):
    class Meta:
        model = SubjectGrade
        exclude = ['reportCardPage']
        labels = {
            'subjectName': ('Subject Name'),
            'marks': ('Marks'),
        }
        help_texts = {
            'subjectName':('Enter the subject name'),
            'marks' : ('Enter the marks'),
        }

class Report_Card_Page_Add_Form(ModelForm):
    class Meta:
        model = ReportCardPage
        exclude = ['reportCard','acknowledgement']
        labels = {
            'examination_type' : ('Examination Name'),
            'exam_date' : ('Date of Exam'),
            'description' : ('Description'),
        }
        help_texts = {
            'examination_type' : ('Enter name of examination'),
            'exam_date' : ('Enter date of examination'),
            'description' : ('Enter a description'),
        }
=======
class StaffAppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    fields = ['apptRejectionReason']
    template_name = "schedule/appointment_reason_update.html"
    success_url = "/schedule/manage=pending/"

    def form_valid(self, form):
        form.instance.apptStatus = self.request.GET.get('status', 'rejected')
        return super().form_valid(form)

    def test_func(self):
        appointment = self.get_object()
        planner = EventPlanner.objects.get(user__exact = self.request.user.id)
        if appointment.eventPlanner_id == planner.id:
            return True
        return False    

>>>>>>> master

######################### Lawrann #########################
# #This form is used to create new appointments
class AppointmentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        if 'stafflist' in kwargs:
            stafflist = kwargs.pop('stafflist',None)
            super(AppointmentForm,self).__init__(*args, **kwargs)
            self.fields['stafflist'] = forms.ChoiceField(choices = stafflist,label = 'Staff Name')

    class Meta:
        model = Appointment
        exclude = ['apptStatus', 'parent', 'apptRejectionReason', 'eventPlanner']

        labels = {
            'apptTitle': ('Appointment Title'),
            'apptDescription': ('Appointment Description'),
            'apptLocation': ('Location of Appointment'),
            'apptDate': ('Date of Appointment'),
            'apptTimeFrom': ('Start Time of Appointment'),
            'apptTimeTo': ('End Time of Appointment'),
        }
        help_texts = {
            'apptTitle':('The title of the appointment goes here.'),
            'apptDescription' : ('The details of the appointment goes here.'),
            'apptLocation': ('The location details of appointment goes here.'),
            'apptDate': ('The date of the appointment goes here.'),
            'apptTimeFrom': ('The start time of the appointment goes here.'),
            'apptTimeTo' : ('The end time of the appointment goes here.'),
        }

class AppointmentUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Appointment
    success_url = reverse_lazy('appointment-manage')
    fields = [
    'apptTitle',
    'apptDescription',
    'apptDate',
    'apptLocation',
    'apptTimeFrom',
    'apptTimeTo'
    ]

    def test_func(self):
        appointment = self.get_object()
        if self.request.user.is_staff == True:
            return False
        if appointment.parent.user != self.request.user or appointment.apptStatus != 'pending':
            return False
        return True


# This class form is used by appointment-approved/pending-delete to delete existing appointment
class AppointmentPendingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment-manage')
    def test_func(self):
        appointment = self.get_object()
        if appointment.parent.user == self.request.user and appointment.apptStatus == 'pending':
            return True
        return False

class AppointmentApprovedDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment-manage=approved')
    def test_func(self):
        appointment = self.get_object()
        if appointment.parent.user == self.request.user and appointment.apptStatus == 'approved':
            return True
        return False  

class ReportCardPageAcknowledgementView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReportCardPage
    success_url = reverse_lazy('childs')
    fields = [
    'acknowledgement'
    ]
    def test_func(self):
        reportcardpage = self.get_object()
        if self.request.user.is_staff == True:
            return False
        # if appointment.parent.user != self.request.user or appointment.apptStatus != 'pending':
        #     return False
        return True
######################### Lawrann #########################
