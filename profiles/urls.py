from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='profile'),
]