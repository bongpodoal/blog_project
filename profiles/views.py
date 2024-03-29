import os

from PIL import Image
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import UpdateView

from do_it_django_prj import settings
from .forms import ProfileForm
from .models import Profile


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # user_id 기준으로 사용자를 검색하여 profiles 리스트에 저장
    profiles = Profile.objects.filter(user=user)

    # profiles 리스트가 비어 있지 않으면 profiles[0]을 사용
    # user_id를 기준으로 정확히 1개의 프로필만 검색되기 때문에 profiles[0]은 해당 프로필을 가리키게 됩니다.
    if profiles:
        profile = profiles.first()
        context = {
            'profile': profile,
            'extra_points': profile.extra_points, # 추가
        }

        return render(request, 'profiles/profile.html', context)
    # profiles 리스트가 비어 있으면 404 오류 발생
    else:
        return render(request, 'profiles/profile.html')
'''
class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'profiles/create_profile.html'
    fields = ['profile_image', 'bio', 'location', 'birthdate']
    def get_success_url(self):
        return reverse('profiles:profile', kwargs={'user_id': self.object.user_id})
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
'''
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'


    def get_success_url(self):
        # 프로필 페이지로 리다이렉트합니다.
        return reverse('profile', kwargs={'user_id': self.request.user.id})

    def form_valid(self, form):
        # 프로필 이미지 업로드 처리
        profile_image = self.request.FILES.get('profile')
        if profile_image:
            img = Image.open(profile_image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(os.path.join(settings.MEDIA_ROOT, 'profile', f'{self.object.user.id}_profile.jpg'), quality=60)
            self.object.profile_image = f'profile/{self.object.user.id}_profile.jpg'
        return super().form_valid(form)
'''
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})

    def form_valid(self, form):
        if 'profile_image' in self.request.FILES:
            profile_image = self.request.FILES['profile_image']
            img = Image.open(profile_image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(os.path.join(settings.MEDIA_ROOT, 'profile_images', str(self.request.user.id) + '_profile.jpg'), quality=60)
            self.object.profile_image = 'profile_images/' + str(self.request.user.id) + '_profile.jpg'
        return super().form_valid(form)
'''