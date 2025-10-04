from django.shortcuts import render
from blog.models import Post


def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]

    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
        }
    )


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )


def eunjun(request):
    return render(request, 'single_pages/eunjun.html')

def siyoon(request):
    return render(request, 'single_pages/siyoon.html')

def jaehyeong(request):
    return render(request, 'single_pages/jaehyeong.html')