"""
URL configuration for fitmatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as h
from authentication import views as a
from survey import views as s
from usersdetails import views as ud
from cal import views as ca

urlpatterns = [
    path('', h.home_view),
    path('help/', h.helpView, name='help'),
    path('authentication/login', a.loginView, name='login'),
    path('authentication/signup', a.signupView, name='signup'),
    path('authentication/logout', a.logoutView, name='logout'),
    path('authentication/reset_password', a.forgotPasswordView, name='reset password'),
    path('survey/', s.surveyView, name='survey'),
    path('edit-survey/', s.editSurveyView, name='edit-survey'),
    path('choose-plan/', s.choosePlanView, name='choose-plan'),
    path('user-details/', ud.userDetailsView, name='user-details'),
    path('save-user-details/', ud.saveUserDetailsView, name='save-user-details'),
    path('calendar/', ca.calendarView, name='calendar'),
    path('addEvent/', ca.addEvent, name='addEvent'),
    path('editEvent/', ca.editEvent, name='editEvent'),
    path('admin/', admin.site.urls),
]
