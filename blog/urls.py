from django.urls import path
from . import views
urlpatterns = [
    path('', views.blog_list,name='blog_list'),
    path('<int:blog_id>', views.blog,name='blog'),
    path('type/<int:blogs_type_id>',views.blogs_with_type,name='blogs_with_type' ),
    path('date/<int:year>/<int:month>',views.blogs_with_date,name='blogs_with_date'),

]