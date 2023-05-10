from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from profiles import views
from profiles.views import ProfileUpdateView

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('profiles/<user_id>/', views.profile, name='profile'),
    # path('profiles/create/', ProfileCreateView.as_view(), name='create_profile'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('single_pages.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

