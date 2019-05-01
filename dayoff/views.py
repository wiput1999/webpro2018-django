from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from dayoff.models import Dayoff
from dayoff.forms import DayOffForm


def index(request):
    context = {}

    try:
        context['dayoff_list'] = Dayoff.objects.all().filter(
            create_by=User.objects.get(username=request.user.username)
        )
    except User.DoesNotExist:
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
            return redirect('index')

    else:
        form = DayOffForm()

    context['form'] = form

    return render(request, template_name='dayoff/create.html', context=context)


def my_login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # Login success null if failed
        if user:
            login(request, user)

            next_url = request.POST.get('next_url')

            if next_url:
                return redirect(next_url)

            if user.groups.filter(name='Manager').exists():
                return redirect('/admin')
            return redirect('index')

        else:
            context['username'] = username
            context['error'] = 'Wrong username or password'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, 'dayoff/login.html', context=context)
