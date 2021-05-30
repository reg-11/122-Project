from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile, Post, Comment


CATEGORIES = [
	('sell', 'sell'),
	('find', 'find'),
	('services', 'services/rent'),
	('swap', 'swap'),
]

# PROBLEMS = [
# 		('hate speech', 'hate speech'),
# 		('violence', 'violence'),
# 		('harassment', 'harassment'),
# 		('nudity', 'nudity'),
# 		('false information', 'false information'),
# 		('Others', 'Others')
# ]


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
		fields = ['body']

		widgets = {
			# 'commenter': forms.TextInput(attrs={'class': 'form-control'}),
			'body': forms.Textarea(attrs={'rows':3, 'class': 'form-control', 'style': 'width:93%;margin-left:35px'}),	
		}

# class ReportForm(forms.ModelForm):
# 	class Meta:
# 		model = Report
# 		problem = forms.ChoiceField(choices=PROBLEMS)
# 		fields = ['problem', 'other_problem']

# 		widgets = {
# 			'other_problem': forms.Textarea(attrs={'rows':3, 'class': 'form-control', 'style': 'width:93%;margin-left:35px'}),	
# 		}



class CreatePostForm(forms.ModelForm):

	class Meta:
		model = Post
		category = forms.ChoiceField(choices=CATEGORIES)
		
		fields = ['category', 'description', 'tags','post_image']

		widgets = {
			'description': forms.Textarea(attrs={'class': 'form-control', 'rows':4}),	
			'tags': forms.TextInput(attrs={'class': 'form-control'}),
			'post_image': forms.FileInput(attrs={'class': 'form-control'}),
		}



	
