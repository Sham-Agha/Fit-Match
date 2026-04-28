from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Question, Video, Plan
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate
from survey.models import PlanOptions



def chooseVideos(request, LIMIT = 1):
    answers = request.session.get("answers")
    print("ans: ",answers)
    focus = time = equipment = discomfort = ""
    for ans in answers:
        
        if ans in ["Build Muscle", "General Fitness", "Improve Academic Endurance", "Reduce Stress"]:
            focus = ans
        elif ans in ["5-10 minutes", "10-20 minutes", "20-30 minutes"]:
            time = ans
        elif ans in ["Dumbbells", "Resistance Bands", "No Equipment"]:
            equipment = ans
        elif ans in ["No Discomfort", "Back Pain", "Leg Pain", "Fatigue/Anxiety"]:
            discomfort = ans
        else:
            continue
    print("[]",focus, time, equipment, discomfort)
    focus_filter = Q(focus__icontains=focus)
    if time == "5-10 minutes":
        time_filter = Q(time__icontains="5 minutes") | Q(time__icontains="10 minutes")
    if time == "10-20 minutes":
        time_filter = Q(time__icontains="10 minutes") | Q(time__icontains="20 minutes")
    if time == "20-30 minutes":
        time_filter = Q(time__icontains="20 minutes") | Q(time__icontains="30 minutes")
    """
    if discomfort, then two discomfort and two normal
    else four normal
    """
    if discomfort == "No Discomfort":
        print("Plans with no discomfort")
        plans = Plan.objects.select_related('video').filter(
                focus_filter,
                time_filter,
                equipment__icontains=equipment,
            )[:4]
    else:
        if equipment == "No Equipment":
            print("plans with discomfort")
            plans = Plan.objects.select_related('video').filter(
                focus_filter,
                #time_filter,
                #equipment__icontains=equipment,
                discomfort=discomfort
            )[:4]
        else:
            print("plans with 1/2 & 1/2 discomfort")
            no_discomfort_plans = list(Plan.objects.select_related('video').filter(
                focus_filter,
                time_filter,
                equipment__icontains=equipment,
                discomfort="No Discomfort"
            )
            )[:LIMIT]
            print("ND", no_discomfort_plans)

            discomfort_plans = list(Plan.objects.select_related('video').filter(
                time_filter,
                discomfort=discomfort
            )
            )[:LIMIT]
            print("DP", discomfort_plans)
            plans = no_discomfort_plans + discomfort_plans
            plan_ids = [p.id for p in plans]
            plans = Plan.objects.filter(id__in=plan_ids).select_related('video')
            print(plans)
    return plans

def surveyView(request):
    questions = Question.objects.prefetch_related("choices").all()
    paginator = Paginator(questions, 3)

    if request.method == "GET":
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(1)
        request.session["answers"] = []
        request.session["survey_complete"] = False
        return render(request, "survey.html", {
            "page_obj": page_obj,
            "page_number": page_number
        })
    
    if request.method == "POST":
        page_number = request.POST.get("page", 1)
        page_number = int(page_number) + 1
        for k in request.POST.keys():
            if k.startswith('question_'):
                request.session.get("answers").append(request.POST.get(k))
                request.session.modified = True

        if page_number > paginator.num_pages:
            request.session["survey_complete"] = True
            plans = chooseVideos(request)
            print("plans", plans)
            request.session["plans"] = list(plans.values_list('id', flat=True))
            return render(request, "survey-complete.html", {
                "plans": plans[:2]
            })

        page_obj = paginator.get_page(page_number)
        return render(request, "survey.html", {
            "page_obj": page_obj,
            "page_number": page_number
        })

@login_required
def choosePlanView(request):
    
    plans = Plan.objects.filter(planoptions__user=request.user).select_related("video")[:4]
    title = 'Fitness Dashboard'
    return render(request, 'choose-plan.html', context={'plans': plans, 'title': title})

def editSurveyView(request):
    questions = Question.objects.prefetch_related("choices").all()
    paginator = Paginator(questions, 3)
    if request.method == "GET":
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(1)
        request.session["answers"] = []
        return render(request, "edit-survey.html", {
            "page_obj": page_obj,
            "page_number": page_number,
            'title': 'Reset Plan'
        })
    
    if request.method == "POST":
        page_number = request.POST.get("page", 1)
        page_number = int(page_number) + 1
        for k in request.POST.keys():
            if k.startswith('question_'):
                request.session.get("answers").append(request.POST.get(k))
                request.session.modified = True    
        if page_number > paginator.num_pages:
            plans = chooseVideos(request, LIMIT=2)
            plan_ids = list(plans.values_list('id', flat=True))
            plan_options = PlanOptions.objects.filter(user=request.user).first()
            plan_options.plans.set(plan_ids)
            return redirect('choose-plan')


        page_obj = paginator.get_page(page_number)
        return render(request, "edit-survey.html", {
            "page_obj": page_obj,
            "page_number": page_number,
            'title': 'Reset Plan'
        })
    return render(request, 'edit-survey.html', {'title': 'Reset Plan'})