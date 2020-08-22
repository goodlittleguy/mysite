from django.contrib import admin
from . import models

@admin.register(models.ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = [
        'read_num','content_object'
    ]\



@admin.register(models.ReadDetail)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = [
        'date','read_num','content_object'
    ]


