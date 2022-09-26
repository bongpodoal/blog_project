from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# 사용자에게 post_list.html 보여줍니다
class PostList(ListView):
    model = Post
    ordering = '-pk'


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
