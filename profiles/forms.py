import os

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from .models import Profile
from django import forms
from django.core.files.base import ContentFile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birthdate', 'location', 'profile_image']

    def clean_profile_image(self):
        f = self.cleaned_data.get("profile_image")
        if not f:
            return f

        # Pillow로 열기 + EXIF 기반 회전 교정
        img = Image.open(f)
        img = ImageOps.exif_transpose(img)

        # 필요시 리사이즈 (예: 긴 변 1080)
        max_side = 1080
        if max(img.size) > max_side:
            img.thumbnail((max_side, max_side))

        from io import BytesIO
        buf = BytesIO()

        # 확장자/포맷 결정
        original_name = getattr(f, "name", "upload")
        base, ext = os.path.splitext(original_name.lower())

        # 알파 채널이 있으면 PNG로 저장
        if img.mode in ("RGBA", "LA"):
            img.save(buf, format="PNG", optimize=True)
            new_name = base + ".png"
            content_type = "image/png"
        else:
            # JPEG로 저장 (필요 시 RGB로 변환)
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            img.save(buf, format="JPEG", quality=85, optimize=True, progressive=True)
            new_name = base + ".jpg"
            content_type = "image/jpeg"

        buf.seek(0)
        return ContentFile(buf.read(), name=new_name)
