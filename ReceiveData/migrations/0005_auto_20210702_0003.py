# Generated by Django 2.2.10 on 2021-07-02 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_delete_userresponse'),
        ('ReceiveData', '0004_auto_20210702_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponse',
            name='question',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.Question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userresponse',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.User'),
            preserve_default=False,
        ),
    ]