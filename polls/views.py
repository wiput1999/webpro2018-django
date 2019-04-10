from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from polls.forms import PollForm
from polls.models import Poll, Question, Answer


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
