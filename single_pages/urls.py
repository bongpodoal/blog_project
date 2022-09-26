from django.urls import path
from . import views
urlpatterns = [
    path('about_me/', views.about_me),
    path('', views.landing),
]
# 도메인 뒤에 아무것도 없을 때는 landing 함수를, 뒤에 about_me/ 가 붙었을 경우에는 about_me 함수를 실행한다.