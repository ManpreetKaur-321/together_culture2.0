from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    interests = forms.ChoiceField(
        choices=[
            ('ARTS', 'Arts & Culture'),
            ('TECH', 'Technology'),
            ('BUSINESS', 'Business & Entrepreneurship'),
            ('EDUCATION', 'Education'),
            ('HEALTH', 'Health & Wellness'),
            ('ENVIRONMENT', 'Environment & Sustainability'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'interests']

class CustomLoginForm(AuthenticationForm):
    is_admin = forms.BooleanField(
        required=False,
        label='Login as Administrator',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Check this box to access admin features'
    ) 