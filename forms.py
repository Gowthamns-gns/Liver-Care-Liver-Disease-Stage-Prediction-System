from django import forms
from .models import PatientRecord
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        exclude = [ 'stage', 'date']
        widgets = {
            'status': forms.Select(choices=[('C', 'Censored'), ('CL', 'Censored due to liver transplant'), ('D', 'Death')]),
            'drug': forms.Select(choices=[('D-penicillamine', 'D-penicillamine'), ('Placebo', 'Placebo')]),
            'sex': forms.Select(choices=[('M', 'Male'), ('F', 'Female')]),
            'ascites': forms.Select(choices=[('N', 'No'), ('Y', 'Yes')]),
            'hepatomegaly': forms.Select(choices=[('N', 'No'), ('Y', 'Yes')]),
            'spiders': forms.Select(choices=[('N', 'No'), ('Y', 'Yes')]),
            'edema': forms.Select(choices=[('N', 'No edema and no diuretic therapy'), ('S', 'Edema present without diuretics or resolved by diuretics'), ('Y', 'Edema despite diuretic therapy')]),
        }
