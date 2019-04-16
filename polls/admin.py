from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission

from polls.models import Poll, Choice, Question, Comment

admin.site.register(Permission)


# Poll Admin
class PollInline(admin.StackedInline):
    model = Question
    extra = 1


class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date', 'end_date', 'del_flag']
    list_per_page = 10

    list_filter = ['start_date', 'end_date', 'del_flag']
    search_fields = ['title']

    # Show only want
    # fields = ['title', 'del_flag']

    # Exclude only don't want
    # exclude = ['del_flag']

    # Just group it
    fieldsets = (
        ('Information', {'fields': ['title', 'del_flag']}),
        ('Active Duration', {'fields': ['start_date', 'end_date'], 'classes': ['collapse']}),
    )

    # Add another model (need to create class)
    inlines = [PollInline]


admin.site.register(Poll, PollAdmin)


# Question Admin
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'poll', 'text']
    list_per_page = 15
    search_fields = ['text']

    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)


# Choice Admin
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'value']
    list_per_page = 15
    list_filter = ['value']
    search_fields = ['question', 'text']


admin.site.register(Choice, ChoiceAdmin)


# Comment Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'email', 'tel', 'poll']
    list_per_page = 15
    list_filter = ['poll']
    search_fields = ['title']


admin.site.register(Comment, CommentAdmin)
