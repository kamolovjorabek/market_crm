from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'password1', 'password2')

    def save(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if (not password1 or not password2) or (password1 != password2):
            raise forms.ValidationError("Password error")
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        phone = self.cleaned_data.get('phone')
        user = self.Meta.model.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role='director',
                password=password1
            )
        user.save()
