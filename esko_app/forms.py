from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms




class CreateUserForm(UserCreationForm):
	password1 =  forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
	password2 =  forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm Password'}))
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}),
			'email': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter UP email'}),
			
		}

	def clean_email(self, *args, **kwargs):
		email = self.cleaned_data.get("email")
		if not email.endswith("@up.edu.ph"):
			raise forms.ValidationError("This is not a valid email")
		return email
