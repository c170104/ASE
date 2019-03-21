from django.contrib import admin
from .models import *
from .forms import UserAdmin

# Register your models here.
# Example Below
admin.site.register(User, UserAdmin)
admin.site.register(ParentProfile)
admin.site.register(Class)
admin.site.register(SubjectClass)
admin.site.register(StaffProfile)
admin.site.register(Student)
admin.site.register(StudentToSubjectClass)
admin.site.register(ReportCard)
admin.site.register(ReportCardPage)
admin.site.register(SubjectGrade)
admin.site.register(Comment)
admin.site.register(Attendance)
admin.site.register(Event)
admin.site.register(EventPlanner)
admin.site.register(Announcement)
admin.site.register(Appointment)