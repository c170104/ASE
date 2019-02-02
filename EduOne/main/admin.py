from django.contrib import admin
from .models import *

# Register your models here.
# Example Below
admin.site.register(ParentProfile)
admin.site.register(StaffProfile)
admin.site.register(Student)
admin.site.register(StudentToStaffSubject)
admin.site.register(ReportCardPage)
admin.site.register(SubjectGrade)
admin.site.register(Comment)