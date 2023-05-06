from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, UpdateView

from .forms import ProfileUpdateForm
from .models import Profile


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # user_id 기준으로 사용자를 검색하여 profiles 리스트에 저장
    profiles = Profile.objects.filter(user__id=user_id)

    # profiles 리스트가 비어 있지 않으면 profiles[0]을 사용
    # user_id를 기준으로 정확히 1개의 프로필만 검색되기 때문에 profiles[0]은 해당 프로필을 가리키게 됩니다.
    if profiles:
        profile = profiles[0]
        context = {
            'profile': profile,
        }
        return render(request, 'profiles/profile.html', context)
    # profiles 리스트가 비어 있으면 404 오류 발생
    else:
        return render(request, 'profiles/profile.html')
