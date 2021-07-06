from django.db import models
from app.models import Question, User, Group
# Create your models here.
class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_feeling = models.IntegerField()
    response_summary = models.CharField(max_length=200)
    response_time = models.DateTimeField(auto_now_add=True)
