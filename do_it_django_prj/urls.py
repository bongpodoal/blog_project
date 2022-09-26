"""
이곳은 사용자가 URL에 접속하였을때 어떻게 웹 사이트를 작동시킬지를 정리해 놓은 파일입니다
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
]
