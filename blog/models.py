from PIL.Image import Image
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os

from profiles.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
    class Meta:
        verbose_name_plural = 'categories'
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
    def get_content_markdown(self):
        return markdown(self.content)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1344/6d2e1cef446711e6/svg/{self.author.email}'


class Comment(models.Model):  # 댓글을 달았을 때 정보를 데이터베이스에 저장합니다. 형식: comment.model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   # 게시물
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 저자
    content = models.TextField()  # 내용
    created_at = models.DateTimeField(auto_now_add=True) # 만든 시간
    modified_at = models.DateTimeField(auto_now=True) # 수정된 시간
    def __str__(self):
        return f'{self.author}::{self.content}'
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}' # 댓글을 달았을 때 #comment-? 위치로 이동한다는 정보를 view에 보냅니다
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1344/6d2e1cef446711e6/svg/{self.author.email}'