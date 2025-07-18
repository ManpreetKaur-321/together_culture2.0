from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MemberProfile

# Create your views here.

@login_required
def dashboard(request):
    profile = MemberProfile.objects.get(user=request.user)
    return render(request, 'members/dashboard.html', {'profile': profile})
