from django.db import models
from embed_video.fields  import EmbedVideoField
from django.contrib.auth.models import User

class Question(models.Model):
    question = models.CharField(max_length=300)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = EmbedVideoField()

class Plan(models.Model):
    focus = models.CharField(max_length=255)
    recommendation = models.CharField(max_length=255, null=True)
    description = models.TextField()
    time = models.CharField(max_length=255)
    discomfort = models.CharField(max_length=255)
    equipment = models.CharField(max_length=255)
    intensity = models.CharField(max_length=255)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class PlanOptions(models.Model):
    user = models.ManyToManyField(User)
    plans = models.ManyToManyField(Plan)
