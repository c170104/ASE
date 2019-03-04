from django import forms
from django.forms import ModelForm
from .models import Event, Announcement

#This form is used by the views.schedule_add to add create new Event objects
class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['eventPlanner']
        labels = {
            'description': ('Event Description'),
            'eventDate': ('Date of Event'),
            'timeFrom': ('Start Time of Event'),
            'timeTo': ('End Time of Event'),
        }
        help_texts = {
            'description' : ('The details of the event goes here.'),
            'eventDate' : ('The date of the event goes here.'),
            'timeFrom' : ('The start time of the event goes here.'),
            'timeTo' : ('The end time of the event goes here.'),
        }


#This form is used by the views.schedule_add to add create new Announcement objects
class AnnoucementForm(ModelForm):
    class Meta:
        model = Announcement
        exclude = ['creator']
        labels = {
            'description': ('Announcement Description'),
            'isEvent' : ('Is this announcement part of a event?'),
            'eventDate': ('Date of Announcement'),
            'eventTimeFrom': ('Start Time of Announcement'),
            'eventTimeTo': ('End Time of Announcement'),
        }
        help_texts = {
            'description': ('The announcement description goes here.'),
            'isEvent' : ('Specifies whether a not the announcement is part of a event.'),
            'eventDate': ('The date of the announcement goes here.'),
            'eventTimeFrom': ('The time where the announcement\'s event(s) starts goes here.'),
            'eventTimeTo': ('The time where the announcement\'s event(s) ends goes here.'),
        }