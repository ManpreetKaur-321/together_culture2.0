"""
URL configuration for together_culture2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.views import register, CustomLoginView, custom_logout
from members.views import dashboard, cancel_booking, profile, manage_members, member_detail, benefits_dashboard, digital_content
from events.views import event_list, book_event
from dashboard.views import admin_dashboard, test_view, debug_admin_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('profile/', profile, name='profile'),
    path('benefits/', benefits_dashboard, name='benefits_dashboard'),
    path('digital-content/', digital_content, name='digital_content'),
    path('events/', event_list, name='event_list'),
    path('events/book/<int:event_id>/', book_event, name='book_event'),
    path('test-dashboard/', test_view, name='test_dashboard'),
    path('debug-admin/', debug_admin_dashboard, name='debug_admin_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('manage-members/', manage_members, name='manage_members'),
    path('member-detail/<int:member_id>/', member_detail, name='member_detail'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
