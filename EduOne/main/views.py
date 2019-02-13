from django.shortcuts import render
from .models import ReportCardPage, SubjectGrade

# Create your views here.
def main(request):
    return render(request, '/', 'hello')
