# Generated by Django 2.1.5 on 2019-02-13 05:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectclass',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 2, 13, 5, 37, 25, 702900, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='commentDate',
            field=models.DateField(default=datetime.datetime(2019, 2, 13, 5, 37, 25, 701127, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='commentTime',
            field=models.TimeField(default=datetime.datetime(2019, 2, 13, 5, 37, 25, 701181, tzinfo=utc)),
        ),
    ]
