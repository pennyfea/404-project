# Generated by Django 2.1.5 on 2019-04-07 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='accessible_users',
        ),
        migrations.AddField(
            model_name='post',
            name='accessible_users',
            field=models.CharField(default=False, max_length=250),
        ),
    ]
