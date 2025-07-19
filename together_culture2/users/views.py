from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
from .forms import CustomUserCreationForm, CustomLoginForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.MEMBER  # Set default role
            user.save()
            
            # The signal will automatically create the MemberProfile
            # Now update the profile with the form data
            from members.models import MemberProfile
            member_profile = MemberProfile.objects.get(user=user)
            member_profile.interests = form.cleaned_data['interests']
            member_profile.save()
            
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Together Culture.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    """Custom logout view to handle logout properly"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomLoginForm
    
    def get_success_url(self):
        # Check if user checked the admin checkbox
        is_admin_login = self.request.POST.get('is_admin') == 'on'
        
        if is_admin_login:
            # If admin checkbox is checked, redirect to admin dashboard
            return '/admin-dashboard/'
        else:
            # If not checked, redirect based on user's actual role
            if self.request.user.role == User.ADMIN:
                return '/admin-dashboard/'
            else:
                return '/dashboard/'
    
    def form_valid(self, form):
        """Override to handle role-based login with validation"""
        # Get the admin checkbox value
        is_admin_login = form.cleaned_data.get('is_admin', False)
        
        # Authenticate the user first
        response = super().form_valid(form)
        
        # After authentication, check if user has admin privileges
        if is_admin_login and self.request.user.role != User.ADMIN:
            # User checked admin but doesn't have admin privileges
            messages.error(self.request, 'Access denied. You do not have administrator privileges.')
            logout(self.request)  # Log them out
            return redirect('login')
        
        # Add a message based on login type
        if is_admin_login:
            messages.success(self.request, 'Logged in as Administrator.')
        else:
            messages.success(self.request, 'Logged in successfully.')
        
        return response
