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

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    # pk는 페이지숫자

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }

    )
# 이 함수로 페이지/세부페이지 를 사용할수 있게끔 합니다.

# Create your views here.
