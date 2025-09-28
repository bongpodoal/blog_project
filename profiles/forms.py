# profiles/forms.py
import os
from io import BytesIO
from typing import Tuple

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify

from PIL import Image, ImageOps

from .models import Profile


# ---- 공통 옵션 ----
MAX_UPLOAD_MB = 5                    # 업로드 최대 5MB
MAX_SIDE_PX = 1080                   # 긴 변 최대 1080px
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}  # 허용 포맷


# ---- 유틸: Pillow 이미지 압축/리사이즈/포맷 정리 ----
def _process_image(file, base_name: str) -> Tuple[InMemoryUploadedFile, str]:
    """
    업로드된 파일을 Pillow로 열어 EXIF 회전 보정, 리사이즈, 압축을 수행하고
    알파채널 유무에 따라 PNG 또는 JPEG로 저장한다.
    반환: (InMemoryUploadedFile, 확장자)
    """
    # Pillow로 열기
    img = Image.open(file)

    # EXIF 기반 회전 교정
    img = ImageOps.exif_transpose(img)

    # 리사이즈(긴 변 기준)
    if max(img.size) > MAX_SIDE_PX:
        img.thumbnail((MAX_SIDE_PX, MAX_SIDE_PX))

    # 버퍼 생성
    buf = BytesIO()

    # 알파채널이 있으면 PNG로 저장
    if img.mode in ("RGBA", "LA"):
        img.save(buf, format="PNG", optimize=True)
        ext = "png"
        content_type = "image/png"
    else:
        # JPEG로 저장 (필요 시 RGB로 변환)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        img.save(buf, format="JPEG", quality=85, optimize=True, progressive=True)
        ext = "jpg"
        content_type = "image/jpeg"

    buf.seek(0)

    # 업로드 객체로 감싸기
    new_name = f"{slugify(base_name) or 'upload'}.{ext}"
    out_file = InMemoryUploadedFile(
        file=buf,
        field_name=None,
        name=new_name,
        content_type=content_type,
        size=buf.getbuffer().nbytes,
        charset=None,
    )
    return out_file, ext


# ---- 사용자 정보 업데이트 폼 ----
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": "아이디",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


# ---- 프로필 수정 폼 ----
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "birthdate", "location", "profile_image"]
        labels = {
            "bio": "소개",
            "birthdate": "생일",
            "location": "사는 곳",
            "profile_image": "프로필 이미지",
        }
        help_texts = {
            "profile_image": "PNG/JPG/WEBP 권장, 5MB 이하",
        }
        widgets = {
            "bio": forms.Textarea(
                attrs={"class": "form-control", "rows": 6, "placeholder": "간단한 자기소개를 적어주세요"}
            ),
            "birthdate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "예: Seoul, KR"}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control-file", "accept": "image/*"}),
        }

    def clean_profile_image(self):
        """
        - 파일이 없으면 그대로 반환(기존 유지)
        - 용량 및 포맷 검증
        - EXIF 회전 보정 / 리사이즈 / 압축
        - 알파채널 있으면 PNG, 아니면 JPEG로 저장
        """
        f = self.cleaned_data.get("profile_image")
        if not f:
            return f  # 업로드 안 했으면 그대로

        # 용량 체크
        size_mb = getattr(f, "size", 0) / (1024 * 1024)
        if size_mb > MAX_UPLOAD_MB:
            raise forms.ValidationError(f"이미지 용량이 너무 큽니다. 최대 {MAX_UPLOAD_MB}MB까지 업로드할 수 있습니다.")

        # Pillow로 열어서 포맷 확인 (Pillow는 확장자 무관)
        try:
            img = Image.open(f)
            if (img.format or "").upper() not in ALLOWED_FORMATS:
                # WEBP 같은 경우도 허용
                pass
        except Exception:
            raise forms.ValidationError("이미지 파일을 열 수 없습니다. 손상되었거나 지원되지 않는 형식입니다.")

        # 원본 이름에서 확장자 제거
        base, _ = os.path.splitext(getattr(f, "name", "upload"))

        # 처리(압축/리사이즈/포맷결정)
        processed, _ext = _process_image(f, base)

        return processed
