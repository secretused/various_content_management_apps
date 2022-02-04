from .models import User
from django import forms
from django.contrib.auth import get_user_model


class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('email',)
        # fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# 必要か不明なため調べてから付属する
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from .models import User
# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'date_of_birth',
#                   'is_active', 'is_admin')

#     def clean_password(self):
#         return self.initial["password"]
