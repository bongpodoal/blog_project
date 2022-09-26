from django.shortcuts import render
from .models import Post
def index(request):
    posts = Post.objects.all().order_by('-pk')
    # 모델에 있는 모든 레코드를 가져온다.(예:제목,내용,날짜)
    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
        }

    )
# 사용자에게 index.html 보여줍니다
# Create your views here.
