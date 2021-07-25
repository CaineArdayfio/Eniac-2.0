# -*- encoding: utf-8 -*-
"""

"""

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Question, User, Group

class QuestionDate(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

admin.site.register(Question, QuestionDate)
admin.site.register(User)
admin.site.register(Group)
