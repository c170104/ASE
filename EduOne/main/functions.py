from .models import Event, Appointment

##Function which returns the respective calendars of the users
def getCalendarInformation(planner, month, year):
    calendar = {}
    #Retrieves all the event for the current month and year with regards to the dateFrom or dateTo
    calendar['events'] = Event.objects.filter(eventPlanner__exact = planner, dateFrom__year__exact = year,
        dateFrom__month__exact = month, dateTo__year__exact = year) | Event.objects.filter(eventPlanner__exact = planner, 
        dateTo__month__exact = month, dateTo__year__exact = year) 

    #Retrieves all the appoinments for the current month and year   
    calendar['appointments'] = Appointment.objects.filter(eventPlanner__exact = planner, apptDate__month__exact = month, 
        apptDate__year__exact = year)   

    return calendar  
