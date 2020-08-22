from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=20)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)  # 关联这两个模型,得到这个某个具体blog即可得到所有ReadDetail包含这个blog的记录
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_time_changed = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('blog', kwargs={'blog_id': self.pk})

    def get_email(self):
        try:
            return self.author.email
        except Exception as e:
            return ''

    def __str__(self):
        return self.title

    # 由日期近及远进行排序
    class Meta:
        ordering = ['-created_time']
