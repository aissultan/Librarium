# Generated by Django 4.2 on 2023-04-26 10:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2023, 4, 26, 10, 8, 43, 28742, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]