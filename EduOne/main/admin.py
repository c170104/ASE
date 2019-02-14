from django.contrib import admin
from .models import *

# Register your models here.
# Example Below
admin.site.register(ParentProfile)
admin.site.register(Class)
admin.site.register(SubjectClass)
admin.site.register(StaffProfile)
admin.site.register(Student)
admin.site.register(StudentToSubjectClass)
admin.site.register(ReportCardPage)
admin.site.register(SubjectGrade)
admin.site.register(Comment)
admin.site.register(Attendance)
admin.site.register(Event)
admin.site.register(EventPlanner)
