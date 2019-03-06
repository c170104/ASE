# Generated by Django 2.1.7 on 2019-03-06 18:52

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190306_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 3, 6, 18, 52, 25, 974686, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='commentDate',
            field=models.DateField(default=datetime.datetime(2019, 3, 6, 18, 52, 25, 974686, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='commentTime',
            field=models.TimeField(default=datetime.datetime(2019, 3, 6, 18, 52, 25, 974686, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subjectclass',
            name='classOf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Class'),
        ),
    ]
