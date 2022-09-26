from django.urls import path
from . import views
# views.py 폴더 불러오기

urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
    # 도메인 뒤에 아무것도 붙지 않았을 때, 실행
    # 사용자에게 index.html을 보여 주는 함수
]
