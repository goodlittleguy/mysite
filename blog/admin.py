from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id','type_name']

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'id','title','author','get_read_num','created_time','last_time_changed','blog_type'
    ]

# @admin.register(models.ReadNum)
# class BlogAdmin(admin.ModelAdmin):
#     list_display = [
#         'read_num','blog'
#     ]
