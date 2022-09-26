from django.urls import path
from . import views
# views.py 폴더 불러오기

urlpatterns = [
    path('<int:pk>/', views.single_post_page),
    path('', views.index),
    # 사용자에게 index.html을 보여 주는 함수
]
