# profiles/urls.py

from django.urls import path
from .views import profile, ProfileUpdateView

app_name = 'profiles'

urlpatterns = [
    path('<user_id>/', profile, name='profile'),
    path('<user_id>/update', ProfileUpdateView.as_view(), name='update-profile'),

]