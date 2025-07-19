from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm
from members.forms import MemberProfileForm
from django.contrib.auth.views import LoginView
from .models import User
from members.models import MemberProfile

# Create your views here.

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = MemberProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Check if user already exists
            username = user_form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                user_form.add_error('username', 'A user with this username already exists.')
            else:
                user = user_form.save(commit=False)
                user.role = user.MEMBER
                user.save()
                # The signal will automatically create the MemberProfile
                # Now update the profile with the form data
                profile = MemberProfile.objects.get(user=user)
                profile.interests = profile_form.cleaned_data['interests']
                profile.membership_type = profile_form.cleaned_data['membership_type']
                profile.orientation_info = profile_form.cleaned_data['orientation_info']
                profile.save()
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = MemberProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        if self.request.user.role == User.ADMIN:
            return '/admin-dashboard/'
        else:
            return '/dashboard/'
