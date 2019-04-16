from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s ไม่ใช่เลขคู่', params={'value': value})


class PollForm(forms.Form):
    title = forms.CharField(label='ชื่อโพล', max_length=100, required=True)
    email = forms.CharField(validators=[validators.validate_email])
    no_questions = forms.IntegerField(label='จำนวนคำถาม', min_value=0, max_value=10, required=True)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def clean_title(self):
        title = self.cleaned_data['title']

        if 'ไอทีหมีแพนด้า' not in title:
            raise forms.ValidationError("คุณลืมชื่อคณะ")

        return title

    def clean(self):
        clean_data = super().clean()

        start = clean_data.get('start_date')
        end = clean_data.get('end_date')

        if start and not end:
            raise forms.ValidationError('โปรดเลือกวันที่สิ้นสุด')

        if not start and end:
            raise forms.ValidationError('โปรดเลือกวันที่เริ่มต้น')


class CommentForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(max_length=500)
    email = forms.EmailField()
    tel = forms.CharField(max_length=10)

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')

        if len(tel) != 10:
            raise forms.ValidationError("เบอร์มือถือต้องมี 10 หลักเท่านั้น")

        if not tel.isdigit():
            raise forms.ValidationError("เบอร์มือถือต้องเป็นตัวเลขเท่านั้น")

        return tel

    def clean(self):
        clean_data = super().clean()

        email = clean_data.get('email')
        tel = clean_data.get('tel')

        if not (email or tel):
            raise forms.ValidationError('คุณต้องกรอก Email หรือ Mobile Number')
