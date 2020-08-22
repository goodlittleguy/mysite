from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Comment)
class ComentAdmin(admin.ModelAdmin):
    list_display = [
        'content_object', 'text', 'comment_time', 'user', 'id'
    ]