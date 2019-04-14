from django.contrib import admin

# Register your models here.
from polls.models import Poll, Choice, Question

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)

