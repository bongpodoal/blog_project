from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, UpdateView

from .forms import ProfileUpdateForm
from .models import Profile


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'user': user}
    return render(request, 'profiles/profile.html', context)

class UserProfileView(DetailView):
    model = User
    template_name = 'profiles/profile.html'
    context_object_name = 'user'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile.html'
    context_object_name = 'profile'


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'profiles/profile_update.html'
    context_object_name = 'profile'
    form_class = ProfileUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user