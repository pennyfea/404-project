# Generated by Django 2.1.5 on 2019-03-27 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20190325_0348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['published']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='timestamp',
            new_name='published',
        ),
    ]
