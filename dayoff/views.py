from django.contrib.auth.models import User
from django.shortcuts import render

from dayoff.models import Dayoff
from dayoff.forms import DayOffForm


def index(request):
    context = {}

    try:
        context['dayoff_list'] = Dayoff.objects.all().filter(
            create_by=User.objects.get(username=request.user.username))
        context['user'] = User.objects.get(username=request.user.username)
    except:
        context['dayoff_list'] = None

    return render(request, template_name='dayoff/index.html', context=context)


def create(request):
    context = {}

    if request.method == 'POST':
        form = DayOffForm(request.POST)
        if form.is_valid():
            Dayoff.objects.create(
                reason=form.cleaned_data.get('reason'),
                type=form.cleaned_data.get('type'),
                date_start=form.cleaned_data.get('date_start'),
                date_end=form.cleaned_data.get('date_end'),
                create_by=User.objects.get(username=request.user.username)
            )
            context['success'] = 'Request successfully submitted'

    else:
        form = DayOffForm()

    context['form'] = form
    context['error'] = form.error

    return render(request, template_name='dayoff/create.html', context=context)
