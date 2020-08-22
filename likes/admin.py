from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models. LikeCount)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
         'liked_num', 'content_object'
    ]

