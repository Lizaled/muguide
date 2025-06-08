from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("Два пароля не совпадают."),
    }

    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_("Введите пароль (минимум 6 символов)."),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Введите тот же пароль еще раз для проверки."),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise ValidationError(_("Пароль должен содержать минимум 6 символов."))
        return password1
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:  # Проверяем, что email существует
            if User.objects.filter(email__iexact=email).exists():
                raise ValidationError(_("Пользователь с такой почтой уже существует"))
        return email
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Старый пароль'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Новый пароль'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Подтверждение нового пароля'})

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']