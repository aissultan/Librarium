# Generated by Django 3.2 on 2023-04-27 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_merge_0006_auto_20230427_1746_0010_alter_review_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='date',
        ),
    ]
