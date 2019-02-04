from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ParentProfile(models.Model):
    RELATION_CHOICES = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    contact_number = models.CharField(max_length=20)
    relation = models.CharField(max_length=6, choices=RELATION_CHOICES)


class StaffProfile(models.Model):
    staff_of = models.ManyToManyField(
        'Student', 
        through='StudentToStaffSubject', 
        through_fields=('staff', 'student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)


class Student(models.Model):
    child_of = models.ForeignKey(
        'ParentProfile', 
        null=True, 
        on_delete=models.SET_NULL
    )
    nric = models.CharField(max_length=9, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    home_address = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=20)


class StudentToStaffSubject(models.Model):
    # Create Composite key (staff,student)
    staff = models.ForeignKey(
        'StaffProfile', 
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        'Student', 
        on_delete=models.CASCADE
    )
    subjectName = models.CharField(max_length=50)

class ReportCard(models.Model):
    student = models.OneToOneField(
        'Student', 
        on_delete=models.CASCADE
    )

class ReportCardPage(models.Model):
    reportCard = models.ForeignKey(
        'ReportCard',
        on_delete=models.CASCADE
    )
    examination_type = models.CharField(max_length=20)
    exam_date = models.DateField()
    description = models.CharField(max_length=200)
    acknowledgement = models.BooleanField(default=False)


class SubjectGrade(models.Model):
    reportCardPage = models.ForeignKey(
        'ReportCardPage', 
        on_delete=models.CASCADE
    )
    subjectName = models.CharField(max_length=50)
    marks = models.DecimalField(max_digits=3, decimal_places=1)


class Comment(models.Model):
    student = models.ForeignKey(
        'Student', 
        on_delete=models.CASCADE
    )
    commentBy = models.CharField(max_length=50)
    commentDate = models.DateField(auto_now=True)
    commentTime = models.TimeField(auto_now=True)
    comment = models.CharField(max_length=200)


class Attendance(models.Model):
    pass


class EventPlanner(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,    
    )


class Event(models.Model):
    eventPlanner = models.ForeignKey(
        'EventPlanner',
        on_delete=models.CASCADE,
    )
    eventDate = models.DateField()
    timeFrom = models.TimeField()
    timeTo = models.TimeField()
    description = models.CharField(max_length=200, blank=True, null=True)

class Appointment(models.Model):
    eventPlanner = models.ForeignKey(
        'EventPlanner',
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'ParentProfile',
        on_delete=models.CASCADE,
    )
    apptDate = models.DateField()
    apptTimeFrom = models.TimeField()
    apptTimeTo = models.TimeField()
    apptDescription = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)

