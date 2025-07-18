from django import forms
from .models import MemberProfile

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['interests', 'membership_type', 'orientation_info'] 