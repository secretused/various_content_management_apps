from django import forms
from django.core.exceptions import ValidationError
from mysite.models import User

# ログイン
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class ChangePasswordForm(forms.Form):
    """パスワード変更"""
    current_password = forms.CharField(
        required=True,
        max_length=255,
        min_length=6,
        widget=forms.PasswordInput(),
    )
    new_password = forms.CharField(
        required=True,
        max_length=255,
        min_length=6,
        widget=forms.PasswordInput(),
    )
    confirm_new_password = forms.CharField(
        required=True,
        max_length=255,
        min_length=6,
        widget=forms.PasswordInput(),
    )

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        user = User.objects.get(id=self.user_id)
        if user.username and current_password:
            auth_result = authenticate(
                username=user.username,
                password=current_password,
            )
            if not auth_result:
                raise ValidationError('現在のパスワードが間違っています。')
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        return new_password

    def clean_confirm_new_password(self):
        confirm_new_password = self.cleaned_data['confirm_new_password']
        return confirm_new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            self.add_error(
                field='confirm_new_password',
                error=ValidationError('パスワードが一致しません。'))
        return cleaned_data


# 画像アップロード(modelの定義)
class UploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('account_image',)
