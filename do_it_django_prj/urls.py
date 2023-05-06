from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from profiles import views

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('profiles/<int:user_id>/', views.profile, name='profile'),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('single_pages.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

