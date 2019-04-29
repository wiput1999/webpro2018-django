from django.contrib.auth.models import User
from django.db import models


class Dayoff(models.Model):
    create_by = models.ForeignKey(User, db_column='create_by', on_delete=models.CASCADE, verbose_name='ขอลาโดย')
    reason = models.TextField(blank=False, null=True, verbose_name='เนื่องจาก')

    type_choice = (
        (0, 'ลากิจ'),
        (1, 'ลาป่วย'),
    )

    type = models.SmallIntegerField(choices=type_choice, default=0, verbose_name='ประเภท')

    date_start = models.DateField(blank=False, null=True, verbose_name='ตั้งแต่วันที่')
    date_end = models.DateField(blank=False, null=True, verbose_name='ถึงวันที่')

    approve_status_choice = (
        (0, 'อนุมัติ'),
        (1, 'ไม่อนุมัติ'),
        (2, 'รอการอนุมัติ'),
    )
    approve_status = models.SmallIntegerField(choices=approve_status_choice, default=2, verbose_name='อนุมัติ')

    class Meta:
        db_table = 'dayoff'
