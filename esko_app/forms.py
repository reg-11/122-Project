from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile, Post, Comment




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

class UserUpdateForm(forms.ModelForm):
	# email = forms.TextInput(attrs={'class': 'form-control'})

	class Meta:
		model = User
		fields = ['username', 'email']

		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control'}),
			# 'email': forms.TextInput(attrs={'class': 'form-control'}),		
		}



class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['profile_pic', 'year_level','phone_number','sns_account','bio']

		widgets = {
			'profile_pic': forms.FileInput(attrs={'class': 'form-control', 'style': 'margin-left:15px; width:50%'}),
			'year_level': forms.TextInput(attrs={'class': 'form-control'}),	
			'phone_number': forms.TextInput(attrs={'class': 'form-control'}),	
			'sns_account': forms.TextInput(attrs={'class': 'form-control'}),	
			'bio': forms.Textarea(attrs={'class': 'form-control'}),		
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['commenter', 'body']

		widgets = {
			'commenter': forms.TextInput(attrs={'class': 'form-control'}),
			'body': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:93%;margin-left:35px'}),	
		}
