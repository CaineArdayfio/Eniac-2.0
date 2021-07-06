# Generated by Django 2.2.10 on 2021-06-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('users', models.ManyToManyField(to='app.User')),
            ],
        ),
    ]