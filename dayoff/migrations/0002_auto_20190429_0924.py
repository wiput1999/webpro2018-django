# Generated by Django 2.2 on 2019-04-29 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dayoff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayoff',
            name='create_by',
            field=models.ForeignKey(db_column='create_by', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
