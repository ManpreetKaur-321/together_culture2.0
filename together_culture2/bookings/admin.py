from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['member', 'event', 'booked_at', 'is_approved', 'status']
    list_filter = ['is_approved', 'booked_at']
    search_fields = ['member__user__username', 'event__title']
    actions = ['approve_bookings', 'reject_bookings']
    
    def status(self, obj):
        return 'Approved' if obj.is_approved else 'Pending'
    status.short_description = 'Status'
    
    def approve_bookings(self, request, queryset):
        queryset.update(is_approved=True)
    approve_bookings.short_description = "Approve selected bookings"
    
    def reject_bookings(self, request, queryset):
        queryset.delete()
    reject_bookings.short_description = "Reject selected bookings"
