from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s ไม่ใช่เลขคู่', params={'value': value})


# New Poll Form
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


# New Comment
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


# Change Password Form
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    new_password_confirm = forms.CharField(max_length=50, widget=forms.PasswordInput())

    def clean(self):
        clean_data = super().clean()

        new_password = clean_data.get('new_password')
        new_password_confirm = clean_data.get('new_password_confirm')

        if new_password != new_password_confirm:
            raise forms.ValidationError('รหัสผ่านใหม่ กับ ยืนยันรหัสผ่านใหม่ไม่ตรงกัน')

        if len(new_password) < 8 or len(new_password_confirm) < 8:
            raise forms.ValidationError('รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร')


# Register Form
class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=True)
    line_id = forms.CharField(max_length=100, required=False)
    facebook = forms.CharField(max_length=100, required=False)

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'X'
    GENDERS = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่นๆ')
    )

    gender = forms.ChoiceField(choices=GENDERS, widget=forms.RadioSelect)

    birth_date = forms.DateField(required=False)

    def clean(self):
        clean_data = super().clean()

        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('รหัสผ่าน กับ ยืนยันรหัสผ่านไม่ตรงกัน')
