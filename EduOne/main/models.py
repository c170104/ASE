from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Create your models here.
class User(AbstractUser):
    is_staff = models.BooleanField('Staff status', default=False)
    is_parent = models.BooleanField('Parent status', default=False)


class ParentProfile(models.Model):
    RELATION_CHOICES = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
    )

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
    )
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    relation = models.CharField(max_length=6, choices=RELATION_CHOICES)

    def __str__(self):
        return "{} {}".format(self.lastname, self.firstname)


class Class(models.Model):
    className = models.CharField(max_length=10)

    def __str__(self):
        return "Class: {}".format(self.className)


class SubjectClass(models.Model):
    classOf = models.OneToOneField(
        'Class',
        on_delete=models.CASCADE,
    )
    student = models.ManyToManyField(
        'Student',
        through='StudentToSubjectClass',
        through_fields=('subjectClass', 'student'),
    )
    teacher = models.ForeignKey(
        'StaffProfile',
        null=True,
        on_delete=models.SET_NULL,
    )
    subject = models.CharField(max_length=20)

    def __str__(self):
        return "Class: {}, Subject: {}".format(self.classOf, self.subject)


class StaffProfile(models.Model):

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    form_class = models.ForeignKey(
        'Class',
        null=True,
        on_delete=models.SET_NULL,
    )
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return "{} {}".format(self.lastname, self.firstname)


class Student(models.Model):
    child_of = models.ForeignKey(
        'ParentProfile', 
        null=True, 
        on_delete=models.SET_NULL,
    )
    form_class = models.ForeignKey(
        'Class',
        null=True,
        on_delete=models.SET_NULL,
    )
    
    nric = models.CharField(max_length=9, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    home_address = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=20)

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)


class StudentToSubjectClass(models.Model):
    subjectClass = models.ForeignKey(
        'SubjectClass', 
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        'Student', 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} {}".format(self.subjectClass, self.student)

    class Meta:
        # all db options go here; sort, order by, index etc..
        unique_together = ("subjectClass", "student")


class ReportCard(models.Model):
    student = models.OneToOneField(
        'Student', 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}'s RCard".format(self.student)


class ReportCardPage(models.Model):
    reportCard = models.ForeignKey(
        'ReportCard',
        on_delete=models.CASCADE,
    )
    examination_type = models.CharField(max_length=20)
    exam_date = models.DateField()
    description = models.CharField(max_length=200)
    acknowledgement = models.BooleanField(default=False)

    def __str__(self):
        return "{} | {} | {}".format(self.examination_type, self.exam_date, self.reportCard)


class SubjectGrade(models.Model):
    reportCardPage = models.ForeignKey(
        'ReportCardPage', 
        on_delete=models.CASCADE,
    )
    subjectName = models.CharField(max_length=50)
    marks = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return "{} {}".format(self.reportCardPage, self.subjectName)


class Comment(models.Model):
    student = models.ForeignKey(
        'Student', 
        on_delete=models.CASCADE,
    )
    commentBy = models.CharField(max_length=50)
    commentDate = models.DateField(default=now())
    commentTime = models.TimeField(default=now())
    comment = models.CharField(max_length=200)

    def __str__(self):
        return "Comment by: {} for {}".format(self.commentBy, self.student)


class Attendance(models.Model):
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
    )
    date = models.DateField(default=now())

    def __str__(self):
        return "{} | {}".format(self.date, self.student)
    
    class Meta:
        unique_together = ("student", "date")


class EventPlanner(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,    
    )

    def __str__(self):
        return "{}'s Planner".format(self.user)


class Event(models.Model):
    eventPlanner = models.ForeignKey(
        'EventPlanner',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=50)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    timeFrom = models.TimeField()
    timeTo = models.TimeField()

    def __str__(self):
        return "{}, Date From: {}, Date To: {}, From: {}, To: {}".format(self.eventPlanner, self.dateFrom, self.dateTo, self.timeFrom, self.timeTo)

APPOINTMENT_STATUS = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
    )

class Appointment(models.Model):
    eventPlanner = models.ForeignKey(
        'EventPlanner',
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'ParentProfile',
        on_delete=models.CASCADE,
    )
    apptTitle = models.CharField(max_length=30)
    apptDescription = models.CharField(max_length=200)
    apptDate = models.DateField()
    apptTimeFrom = models.TimeField()
    apptTimeTo = models.TimeField()
    apptStatus = models.CharField(max_length=8, choices= APPOINTMENT_STATUS)

    def __str__(self):
        return "Appt by: {} | Status: {}".format(self.parent, self.apptStatus)


class Announcement(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    dateCreated = models.DateField()

    def __str__(self):
        return "User: {}, title: {}".format(self.user, self.title)

