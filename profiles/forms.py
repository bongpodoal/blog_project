from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile
from django import forms


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
        profile_image = self.cleaned_data.get('profile_image', False)
        if profile_image:
            from PIL import Image
            from io import BytesIO
            from django.core.files.uploadedfile import InMemoryUploadedFile

            # 이미지 파일 읽어오기
            image = Image.open(profile_image)

            # 이미지 크기 변경하기
            image.thumbnail((300, 300))

            # 변경된 이미지를 BytesIO 객체에 쓰기
            output = BytesIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)

            # 변경된 이미지를 InMemoryUploadedFile 객체로 만들기
            profile_image = InMemoryUploadedFile(
                output,
                'ImageField',  # 파일 필드 이름
                f'{self.instance.id}.jpg',  # 파일 이름
                'image/jpeg',
                output.getbuffer().nbytes,
                None
            )

        return profile_image