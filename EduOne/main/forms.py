from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#This form is used by the views.schedule_add to add create new Event objects
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


#This form is used by the views.schedule_add to add create new Announcement objects
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

#This class form is used by event-detail to view event details
class EventDetailView(DetailView):
    model=Event

#This class form is used by announcement-detail to view event details
class AnnouncementDetailView(DetailView):
    model=Announcement

#This class form is used by appointment-detail to view event details
class AppointmentDetailView(DetailView):
    model=Appointment    

#This class form is used by announcement-delete to delete existing announcements
class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    success_url = "/schedule/manage=announcements/"
    
    def test_func(self):
        announcement = self.get_object()
        if self.request.user == announcement.user:
            return True
        return False    

#This class form is used by event-delete to delete existing events
class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = "/schedule/manage=confirmed/"
    
    def test_func(self):
        event = self.get_object()
        user_id = EventPlanner.objects.get(id__exact = event.eventPlanner_id).user_id
        if self.request.user.id == user_id:
            return True
        return False  
