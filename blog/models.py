from django.db import models
from django.contrib.auth.models import User
import os
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    # 게시물의 제목
    content = models.TextField()
    # 게시물의 내용
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # 월,일,시 를 기록할 수 있게 하는 필드

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_absolute_url(self):
        return f'/blog/{self.pk}'
    # 포스트의 제목과 번호를 문자열로 표현
    # author: 추후 추가 예정
