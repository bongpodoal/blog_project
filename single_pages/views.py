from django.shortcuts import render

def landing(request):
    return render(
        request,
        'single_pages/landing.html'
    )
# 도메인 뒤에 아무것도 없을 때 landing.html을 불러옴
def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )

# 도메인 뒤에 about_me가 있을 때 about_me.html을 불러옴