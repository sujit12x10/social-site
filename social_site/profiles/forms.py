from django import forms 
from profiles.models import Profile
from django.forms import Textarea

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar')
        widgets = {
            'bio': Textarea({
                'rows': 1
            })
        }