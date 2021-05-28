from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import User, Post, Comment
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm, CommentForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
	posts = Post.objects.all()
	return render(request, 'esko_app/home.html', {'posts': posts})

class PostListView(ListView):
	model = Post
	template_name = 'esko_app/profile.html' # <app>/model_viewtype.html
	context_object_name = 'posts'
	ordering = ['-date']

class PostDetailView(DetailView):
	model = Post

class PostCreateView(CreateView):
	model = Post
	fields = ['category','description','tags','post_image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	fields = ['category','description','tags','post_image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostUpdateView,self).form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	success_url = '/esko_app/profile'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



def profile(request,pk):
	# getting number of likes 
	get_post = get_object_or_404(Post, id=self.kwargs['pk'])
	total_likes = get_post.total_likes()
	
	context = {
		'posts': posts,
		'total_likes':total_likes
	}


	posts = Post.objects.get(author=request.user)
	return render(request,'esko_app/profile.html', context)

def LikeView(request,pk):
	post = get_object_or_404(Post,id=request.POST.get('post_id'))
	post.likes.add(request.user)

	return redirect('/esko_app/profile/')

	# return HttpResponseRedirect(reverse('profile',args=[str(pk)]))

class AddCommentView(CreateView):
	model = Comment
	form_class= CommentForm
	template_name = 'esko_app/add_comment.html'

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)



	success_url = reverse_lazy("esko_app:post-detail")



def profileSettings(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been updated!')
			return redirect('/esko_app/profileSettings/')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'esko_app/profilesettings.html',context)

