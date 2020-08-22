import threading

from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template.loader import render_to_string


class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.text,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text,
        )


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)  # 谁写的,通过定义related_name
    # 将Django内定义的知道返回该键存储的数据的 小写模型名 + '_set' ,在此即为comment_set方法改名为comments,避免命名冲突,

    root = models.ForeignKey('self', related_name="root_comment", null=True, on_delete=models.CASCADE)
    # 使用方法为某个实例化的 comment.root.all() 得到所有其他的有该root的comment , 见blog.html,86
    parent = models.ForeignKey('self', related_name="parent_comment", null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, null=True, related_name="replies", on_delete=models.CASCADE) # 回复誰

    def send_mail(self):
        # 发送邮件通知
        if self.parent is None:
            subject = '有人评论您的博客'
            email = self.content_object.get_email()
        else:
            subject = '有人回复了您的评论'
            email = self.reply_to.email()
        if email != '':
            context = dict()
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/email.html', context)
            send_mail_do = SendMail(subject, text, email, False)
            send_mail_do.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering =['comment_time']



