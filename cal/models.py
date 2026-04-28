from django.db import models
from django.contrib.auth.models import User
from survey.models import Plan
from datetime import date
# Create your models here.
class Event(models.Model):
    user = models.ManyToManyField(User)
    plan = models.ManyToManyField(Plan)
    date = models.DateField()
