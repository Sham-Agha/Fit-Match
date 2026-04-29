from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import survey_required
from survey.models import PlanOptions


def loginView(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('choose-plan')
        else:
            messages.error(request, "Loggin failed")
            return redirect('login')
        
@survey_required
def signupView(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Account with this email already exists.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Account with this username exists.")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        messages.success(request, "Account created successfully.")
        login(request, user) 
        plan_options = PlanOptions.objects.create()
        plan_options.user.add(user)
        plan_ids = request.session.get("plans")
        plan_options.plans.set(plan_ids)
        return redirect('choose-plan')


def forgotPasswordView(request):
    context = {}
    context["password_reset_success"] = False
    if request.method == "GET":
        return render(request, 'forgotPassword.html', context)
    if request.method == "POST":
        if "email_submit" in request.POST:
            email = request.POST.get("email")

            if User.objects.filter(email=email).exists():
                request.session["reset_email"] = email
                context["show_password_form"] = True
            else:
                messages.error(request, "Email does not exist")
            return render(request, "forgotPassword.html", context)

        elif "password_submit" in request.POST:
            email = request.session.get("reset_email")
            password = request.POST.get("password")

            if email:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                context["password_reset_success"] = True
            return render(request, "forgotPassword.html", context)

    
def logoutView(request):
    logout(request)
    return redirect('login')