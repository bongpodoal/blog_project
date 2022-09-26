"""
이곳은 사용자가 URL에 접속하였을때 어떻게 웹 사이트를 작동시킬지를 정리해 놓은 파일입니다
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('blog/', include('blog.urls')),
    # blog/가 붙었을 떄, blog폴더에 urls.py로 패스합니다
    path('admin/', admin.site.urls),
    path('', include('single_pages.urls')),
    # 도메인 뒤에 아무것도 없을 때 실행되는 url
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
