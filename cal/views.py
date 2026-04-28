from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import calendar
from datetime import date
from django.shortcuts import render
from .models import Event
from survey.models import Plan
from django.contrib.auth import authenticate
@login_required
def calendarView(request):
    print(request.user.username)
    print(authenticate(username='user178', password='user178') == request.user)
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))
    cal = calendar.monthcalendar(year, month)
    events = Event.objects.filter(user=request.user, date__year=year, date__month=month)
    plans = Plan.objects.filter(planoptions__user=request.user)
    print("PP", plans)
    event_dict = {}
    for event in events:
        day = event.date.day
        event_dict.setdefault(day, []).append(event)
    print(event_dict)
    today = date.today()
    if year == today.year and month == today.month:
        month_type = "current"
    elif (year, month) < (today.year, today.month):
        month_type = "past"
    else:
        month_type = "future"

    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    title = 'Calendar'
    context = {
        "calendar": cal,
        "month":month,
        "month_name": calendar.month_name[month],
        "year": year,
        "month_type": month_type,
        "prev_year":prev_year,
        "prev_month":prev_month,
        "next_month": next_month,
        "next_year": next_year,
        "event_dict": event_dict,
        "title": title,
        "plans": plans
    }
    
    return render(request, "calendar.html", context)

def addEvent(request):
    if request.method == "POST":
        day = request.POST.get("day")
        month = request.POST.get("month")
        year = request.POST.get("year")
        plan_id = request.POST.get("plan_id")
        
        event_date = date(int(year), int(month), int(day))

        plan = Plan.objects.filter(id=plan_id)

        event = Event.objects.create(date=event_date)
        event.user.add(request.user)
        event.plan.set(plan)
        print(event)
        return redirect("calendar")
    else:
        print("not POST")
        

def editEvent(request):
    if request.method == "POST":
        day = int(request.POST.get("day"))
        month = int(request.POST.get("month"))
        year = int(request.POST.get("year"))
        plan_id = request.POST.get("plan_id")
        
        event_date = date(year, month, day)

        if plan_id == "-1":
            Event.objects.filter(
                user=request.user,
                date=event_date
            ).delete()
            return redirect("calendar")
        # safely get event
        event = Event.objects.filter(user=request.user, date=event_date)
        plan = Plan.objects.filter(id=plan_id)
        

        # update
        event.date = event_date
        event.save()

        event.plan.set([plan])
        event.user.set([request.user])

        return redirect("calendar")