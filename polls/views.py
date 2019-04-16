from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

from polls.forms import PollForm, CommentForm, ChangePasswordForm, RegisterForm
from polls.models import Poll, Question, Answer, Comment


# Create your views here.
def index(request):
    """

    :param request: object
    :return:
    """
    poll_list = Poll.objects.annotate(question_count=Count('question')).filter(del_flag=False)

    # for poll in poll_list:
    #     question_count = Question.objects.filter(poll_id=poll.id).count()
    #     poll.question_count = question_count

    context = {
        "page_title": "My Polls",
        "poll_list": poll_list
    }

    return render(request, template_name='polls/index.html', context=context)


# Poll Detail
@login_required
@permission_required('polls.view_poll')
def detail(request, poll_id):
    """

    :param request: object
    :param poll_id: number
    :return:
    """

    poll = Poll.objects.get(pk=poll_id)

    for question in poll.question_set.all():
        name = 'choice' + str(question.id)
        choice_id = request.GET.get(name)

        if choice_id:
            try:
                answer = Answer.objects.get(question_id=question.id)
                answer.choice_id = choice_id
                answer.save()
            except Answer.DoesNotExist:
                Answer.objects.create(
                    choice_id=choice_id,
                    question_id=question.id
                )

    context = {
        "poll": poll
    }

    return render(request, template_name='polls/detail.html', context=context)


@login_required
@permission_required('polls.add_poll')
def create(request):
    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            poll = Poll.objects.create(
                title=form.cleaned_data.get('title'),
                start_date=form.cleaned_data.get('start_date'),
                end_date=form.cleaned_data.get('end_date'),
            )

            for i in range(1, form.cleaned_data.get('no_questions') + 1):
                Question.objects.create(
                    text='Q' + str(i),
                    type='01',
                    poll=poll
                )

    else:
        form = PollForm()

    context = {
        'form': form
    }

    return render(request, 'polls/create.html', context=context)


@login_required
def create_comment(request, poll_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment.objects.create(
                title=form.cleaned_data.get('title'),
                body=form.cleaned_data.get('body'),
                tel=form.cleaned_data.get('tel'),
                email=form.cleaned_data.get('email')
            )


    else:
        form = CommentForm()

    context = {
        'form': form,
        'poll_id': poll_id
    }

    return render(request, 'polls/create-comment.html', context=context)


# Login
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

            return redirect('index')

        else:
            context['username'] = username
            context['error'] = 'Wrong username or password'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, 'polls/login.html', context=context)


# Logout
def my_logout(request):
    logout(request)
    return redirect('login')


# Change Password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()

    else:
        form = ChangePasswordForm()

    context = {
        'form': form
    }

    return render(request, 'polls/change-password.html', context=context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            pass

    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'polls/register.html', context=context)
