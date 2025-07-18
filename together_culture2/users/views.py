from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from members.forms import MemberProfileForm
from django.contrib.auth.views import LoginView

# Create your views here.

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = MemberProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = user.MEMBER
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserRegisterForm()
        profile_form = MemberProfileForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
