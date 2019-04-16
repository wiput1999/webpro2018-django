from django.db import models


# Profile
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    line_id = models.CharField(max_length=100)
    facebook = models.CharField(max_length=100)

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'X'
    GENDERS = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่นๆ')
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

    birth_date = models.DateField()


# Poll
class Poll(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    del_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Question
class Question(models.Model):
    text = models.TextField()

    SINGLE = '01'
    MULTIPLE = '02'
    TYPES = ((SINGLE, 'Single answer'), (MULTIPLE, 'Multiple answer'))
    type = models.CharField(max_length=2, choices=TYPES, default='01')
    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)

    def __str__(self):
        return '(%s) %s' % (self.poll.title, self.text)


# Choice
class Choice(models.Model):
    text = models.CharField(max_length=100)
    value = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    def __str__(self):
        return '(%s) %s' % (self.question.text, self.text)


# Answer
class Answer(models.Model):
    choice = models.OneToOneField(Choice, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)


# Comment
class Comment(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.title
