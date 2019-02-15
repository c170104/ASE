from django.shortcuts import render
from .models import ReportCardPage, SubjectGrade

# Create your views here.
def home(request):
    return render(request, 'index.html', {'active_page': 'home'})
