from django.contrib import admin
from .models import Question, Choice, Video, Plan, PlanOptions
# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Video)
admin.site.register(Plan)
admin.site.register(PlanOptions)

