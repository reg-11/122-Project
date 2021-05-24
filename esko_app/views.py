from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User, Post
from .forms import CreateUserForm

# Create your views here.


#landing page
def index(request):
	return render(request, 'esko_app/index.html')

#sign-up page
def signup(request):

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			print('yes')
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account successfully created!')
			return redirect('/esko_app/login/')
			
	else:
		print('no')
		form = CreateUserForm()	
	return render(request, 'esko_app/signup.html', {'form': form})



# login even w wrong creds
# def loginPage(request):
# 	if request.method == 'POST':
# 		email = request.POST['email']
# 		password = request.POST['password']
# 		username = ''
# 		try:
# 			username = User.objects.get(email=email).username
# 		except User.DoesNotExist:
# 			print('none')
# 			messages.info(request, 'email or password is incorrect')
# 		user = authenticate(request, username=username, password=password)
# 		if user is not None:
# 			login(request, user)
# 			# print("Logged in")
# 		# else:
# 		# 	print("not logged in")
# 		return redirect('/esko_app/home/')
# 	else:
# 		return render(request, 'esko_app/login.html')

def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			# correct username and password login the user
			login(request, user)
			return redirect('/esko_app/home/')

		else:
			messages.error(request, 'Error wrong username/password')

	return render(request, 'esko_app/login.html')


def logoutUser(request):
	logout(request)
	return redirect('/esko_app/login/')

def about(request):
	return render(request, 'esko_app/about.html')

# @login_required
def home(request):
	return render(request, 'esko_app/home.html')

def profile(request):
	return render(request, 'esko_app/profile.html')