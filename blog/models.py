from django.db import models
class Post(models.Model):
    title = models.CharField(max_length=30)
    # 게시물의 제목
    content = models.TextField()
    # 게시물의 내용
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 월,일,시 를 기록할 수 있게 하는 필드

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'
    # 포스트의 제목과 번호를 문자열로 표현
    # author: 추후 추가 예정
