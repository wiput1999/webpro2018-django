import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from polls.forms import PollForm, CommentForm, ChangePasswordForm, RegisterForm, PollModelForm, QuestionForm, ChoiceForm
from polls.models import Poll, Question, Answer, Comment, Profile, Choice


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
    question_formset = formset_factory(QuestionForm, min_num=1, max_num=15, extra=0)

    if request.method == 'POST':
        form = PollModelForm(request.POST)
        formset = question_formset(request.POST)

        if form.is_valid():
            poll = form.save()
            if formset.is_valid():
                for i in formset:
                    Question.objects.create(
                        text=i.cleaned_data.get('text'),
                        type=i.cleaned_data.get('type'),
                        poll=poll
                    )
                return redirect('index')
    else:
        form = PollModelForm()
        formset = question_formset()

    context = {
        'form': form,
        'formset': formset,
        'error': form.errors
    }

    return render(request, 'polls/create.html', context=context)


@login_required
@permission_required('polls.change_poll')
def update(request, poll_id):
    question_formset = formset_factory(QuestionForm)
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        form = PollModelForm(request.POST, instance=poll)
        formset = question_formset(request.POST)

        if form.is_valid():
            form.save()

            if formset.is_valid():
                for i in formset:
                    if i.cleaned_data.get('question_id'):
                        question = Question.objects.get(id=i.cleaned_data.get('question_id'))

                        if question:
                            question.text = i.cleaned_data.get('text')
                            question.type = i.cleaned_data.get('type')
                            question.save()
                    elif i.cleaned_data.get('text'):
                        Question.objects.create(
                            text=i.cleaned_data.get('text'),
                            type=i.cleaned_data.get('type'),
                            poll=poll
                        )
                return redirect('update_poll', poll_id=poll_id)

    else:
        form = PollModelForm(instance=poll)
        formset = question_formset(initial=[{'text': i.text, 'type': i.type, 'question_id': i.id}
                                            for i in poll.question_set.all()])
        data = [{'text': i.text, 'type': i.type, 'question_id': i.id}
                for i in poll.question_set.all()]

    context = {
        'poll': poll,
        'form': form,
        'formset': formset,
        'error': form.errors
    }

    return render(request, template_name='polls/update.html', context=context)


@login_required
@permission_required('polls.change_poll')
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect('update_poll', poll_id=question.poll.id)


# Choices
@login_required
def edit_choice(request, question_id):
    question = Question.objects.get(pk=question_id)

    choices = [{'id': i.id, 'text': i.text, 'value': i.value, 'question': i.question_id}
               for i in question.choice_set.all()]

    context = {
        'poll': question.poll,
        'question': question,
        'choices': json.dumps(choices),
    }

    return render(request, template_name='polls/edit-choice.html', context=context)


@csrf_exempt
def edit_choice_api(request, question_id):
    if request.method == 'POST':
        choice_list = json.loads(request.body)
        error_message = None

        # Algorithm: Delete choices
        database_choice_list_ids = [i.id for i in Question.objects.get(pk=question_id).choice_set.all()]
        choice_list_ids = list()

        for i in choice_list:
            try:
                choice_list_ids.append(i['id'])
            except KeyError:
                pass

        for i in database_choice_list_ids:
            if i not in choice_list_ids:
                Choice.objects.get(pk=i).delete()

        # Algorithm: Validations
        for i in choice_list:
            print(type(i['value']))
            if i['text'] == '' or i['value'] == '':
                error_message = 'Fields can\'t be left blank.'
                break
            error_message = None

        # Algorithm: Save choices
        if not error_message:
            for i in choice_list:
                try:
                    # Case: Choice already exists.
                    Choice.objects.filter(pk=i['id']).update(text=i['text'], value=i['value'])
                except KeyError:
                    # Case: Choice doesn't exist.
                    form = ChoiceForm({'text': i['text'],
                                       'value': i['value'],
                                       'question': question_id,})
                    if form.is_valid():
                        form.save()
                    else:
                        error_message = 'Fields can\'t be left blank.'
                        break

        if not error_message:
            return JsonResponse({'message': 'success'}, status=200)
        return JsonResponse({'message': error_message}, status=400)

    return JsonResponse({'message': 'This API doesn\'t accept GET requests.'}, status=405)


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
        form = ChangePasswordForm(request, request.POST)

        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()

    else:
        form = ChangePasswordForm(request)

    context = {
        'form': form
    }

    return render(request, 'polls/change-password.html', context=context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )

            user.set_password(form.cleaned_data.get('password'))

            user.save()

            profile = Profile.objects.create(
                user=user,
                line_id=form.cleaned_data.get('line_id'),
                gender=form.cleaned_data.get('gender'),
                facebook=form.cleaned_data.get('facebook'),
                birth_date=form.cleaned_data.get('birth_date'),
            )

    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'polls/register.html', context=context)
