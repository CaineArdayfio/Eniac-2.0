from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    phone_number = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Group(models.Model):
    group_name = models.CharField(max_length=200, primary_key=True)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.group_name

class Question(models.Model):
    question_name = models.CharField(max_length=200)
    question_text = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)
    time = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.CharField(max_length=200)
    groups = models.ManyToManyField(Group)

    class Meta:
        unique_together = ('question_name','question_text', 'time',)

    def __str__(self):
        return self.question_name
