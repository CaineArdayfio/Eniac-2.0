# Generated by Django 2.2.10 on 2021-06-25 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='users',
        ),
        migrations.AddField(
            model_name='question',
            name='groups',
            field=models.ManyToManyField(to='app.Group'),
        ),
    ]
