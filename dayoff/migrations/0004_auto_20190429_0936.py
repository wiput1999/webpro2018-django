# Generated by Django 2.2 on 2019-04-29 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dayoff', '0003_auto_20190429_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayoff',
            name='approve_status',
            field=models.SmallIntegerField(choices=[(0, 'อนุมัติ'), (1, 'ไม่อนุมัติ'), (2, 'รอการอนุมัติ')], default=2),
        ),
        migrations.AddField(
            model_name='dayoff',
            name='date_end',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='dayoff',
            name='date_start',
            field=models.DateField(null=True),
        ),
    ]
