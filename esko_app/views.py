from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import User, Post, Comment, Report
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm, CommentForm, CreatePostForm, ReportForm

from .filters import PostFilter
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from taggit.models import Tag



# from django.forms import modelformset_factory
# from .forms import ImageForm
# from .models import Images


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


def category(request):
	return render(request, 'esko_app/category.html')

def search_tags(request):
	if request.method == "POST":
		searched = request.POST['searched']
		# tags = Tag.objects.filter()
		return render(request, 'esko_app/search_tags.html', {'searched':searched})
	else:
		return render(request, 'esko_app/search_tags.html', {})



class PostListView(ListView):
	model = Post
	template_name = 'esko_app/profile.html' # <app>/model_viewtype.html
	context_object_name = 'posts'
	ordering = ['-date']


class HomeListView(ListView):
	model = Post
	template_name = 'esko_app/home.html' # <app>/model_viewtype.html
	context_object_name = 'posts'
	ordering = ['-date']


# @login_required(login_url= '/esko_app/login/')
# def home(request):
# 	posts = Post.objects.all().order_by('-date')
# 	# images = Images.objects.all()

# 	for post in posts:

# 		total_likes = post.total_likes()

# 		liked = False
# 		if post.likes.filter(id=request.user.id).exists():
# 			liked = True

# 	filtered_posts = PostFilter(
# 		request.GET,
# 		queryset=posts
# 	)
	
# 	post_paginator = Paginator(filtered_posts.qs, 3)
# 	page_num = request.GET.get('page')
# 	page = post_paginator.get_page(page_num)

# 	context = {
# 		'count' : post_paginator.count,
# 		'page' : page,
# 		'total_likes': total_likes,
# 		'liked': liked,
# 		# 'images': images,
# 	}	
# 	return render(request, 'esko_app/home.html', context)



@login_required(login_url= '/esko_app/login/')
def home(request):
	posts = Post.objects.all().order_by('-date')
	


	for post in posts:

		total_likes = post.total_likes()
		tag_list = post.tag_list()
		# print(tag_list)

		liked = False
		if post.likes.filter(id=request.user.id).exists():
			liked = True

	filtered_posts = PostFilter(
		request.GET,
		queryset=posts
	)
	
	post_paginator = Paginator(filtered_posts.qs, 3)
	page_num = request.GET.get('page')
	page = post_paginator.get_page(page_num)

	context = {
		'count' : post_paginator.count,
		'page' : page,
		'total_likes': total_likes,
		'liked': liked,
		'tag_list': tag_list,
	}	
	return render(request, 'esko_app/home.html', context)

@login_required(login_url= '/esko_app/login/')
def PostByCategory(request):
	posts = Post.objects.all().order_by('-date')


	for post in posts:

		total_likes = post.total_likes()

		liked = False
		if post.likes.filter(id=request.user.id).exists():
			liked = True

	filtered_posts = PostFilter(
		request.GET,
		queryset=posts
	)
	
	post_paginator = Paginator(filtered_posts.qs, 3)
	page_num = request.GET.get('page')
	page = post_paginator.get_page(page_num)

	context = {
		'count' : post_paginator.count,
		'page' : page,
		'total_likes': total_likes,
		'liked': liked,
	}	
	# return render(request, 'esko_app/home.html', context)
	return render(request, 'esko_app/sell.html', context)


class TagIndexView(ListView):
	model = Post
	template_name = 'esko_app/tagView.html' # <app>/model_viewtype.html
	context_object_name = 'posts'
	ordering = ['-date']

	def get_queryset(self):
		return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug'))



def SearchByTag(request):
 
	if request.method == 'GET': # If the form is submitted
		search_query = request.GET.get('search_box', None)
		posts = Post.objects.filter(tags__contains=str(search_query))

		total_likes = 0
		liked = False
		# tag_list = ['tags']
		for post in posts:

			total_likes = post.total_likes()
			# tag_list = post.tag_list()

			liked = False
			if post.likes.filter(id=request.user.id).exists():
				liked = True

		filtered_posts = PostFilter(
			request.GET,
			queryset=posts
		)
		
		post_paginator = Paginator(filtered_posts.qs, 3)
		page_num = request.GET.get('page')
		page = post_paginator.get_page(page_num)

		context = {
			'count' : post_paginator.count,
			'page' : page,
			'total_likes': total_likes,
			'liked': liked,
			'search_query': search_query,
			'tag_list' : post.tag_list(),

		}	
		return render(request, 'esko_app/search_tags.html', context)


@login_required(login_url= '/esko_app/login/')
def profile(request):
	posts = Post.objects.filter(author=request.user).order_by('-date')

	total_likes = 0
	liked = False
	for post in posts:
		total_likes = post.total_likes()
		tag_list = post.tag_list()

		liked = False
		if post.likes.filter(id=request.user.id).exists():
			liked = True

	
	filtered_posts = PostFilter(
		request.GET,
		queryset=posts
	)
	
	post_paginator = Paginator(filtered_posts.qs, 3)
	page_num = request.GET.get('page')
	page = post_paginator.get_page(page_num)

	
	context = {
		'count' : post_paginator.count,
		'page' : page,
		'total_likes': total_likes,
		'liked': liked,
		'tag_list': tag_list
	}
	
	return render(request,'esko_app/profile.html', context)


def profileOther(request,username):
		
	post = get_object_or_404(Post,id=request.POST.get('post_id'))

	total_likes = post.total_likes()
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		liked = True


	posts = Post.objects.filter(author=post.author).order_by('-date')
	print(posts)

	context = {
		'user' : post.author,
		'posts' :posts,
		'total_likes': total_likes,
		'liked': liked,
		'tag_list': post.tag_list(),
	}
	return render(request,'esko_app/other_profile.html', context)


def profileOtherComment(request,username):
	comment = get_object_or_404(Comment,id=request.POST.get('comment_id'))
	comments = Comment.objects.filter(commenter=comment.commenter)

	posts = Post.objects.filter(author=comment.commenter).order_by('-date')
	
	context = {
		'user' : comment.commenter,
		'posts' :posts,
		
	}	
	return render(request,'esko_app/other_profile_comment.html', context)




class PostDetailView(LoginRequiredMixin,DetailView):
	model = Post

	def get_context_data(self,*args, **kwargs):
		context = super(PostDetailView,self).get_context_data()

		# getting number of likes 
		get_post = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = get_post.total_likes()
		tag_list = get_post.tag_list()

		liked = False
		if get_post.likes.filter(id=self.request.user.id).exists():
			liked = True

		context["total_likes"] = total_likes
		context["liked"] = liked
		context["tag_list"] = tag_list
		print(tag_list)
		print(get_post.tags)
		return context



class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	form_class = CreatePostForm
	# fields = ['category','description','tags','post_image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	form_class = CreatePostForm
	# fields = ['category','description','tags','post_image']

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


class ReportPostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	success_url = '/esko_app/reported-posts'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


@login_required(login_url= '/esko_app/login/')
def LikeView(request,pk):
	post = get_object_or_404(Post,id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True


	return HttpResponseRedirect(reverse('esko_app:post-detail',args=[str(pk)]))



class AddCommentView(LoginRequiredMixin,CreateView):
	model = Comment
	form_class= CommentForm
	template_name = 'esko_app/add_comment.html'

	def form_valid(self, form):
		form.instance.commenter = self.request.user
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)
	
	def get_success_url(self, **kwargs):
		return reverse('esko_app:post-detail', kwargs={'pk':self.kwargs['pk']})




@login_required(login_url= '/esko_app/login/')
def reportedPosts(request):
	reports = Report.objects.all().order_by('-date_reported')
	#posts = Post.objects.all(repo_id__pk=rpost.post)

	context = {
		'reports' : reports
	}
	return render(request, 'esko_app/reported-post.html', context)


class ReportView(LoginRequiredMixin,CreateView):
	model = Report
	form_class= ReportForm
	template_name = 'esko_app/add_report.html'

	def form_valid(self, form):
		form.instance.reporter = self.request.user
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)
	
	def get_success_url(self, **kwargs):
		return reverse('esko_app:post-detail', kwargs={'pk':self.kwargs['pk']})


class ReportDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Report
	success_url = '/esko_app/reported-posts'

	def test_func(self):
		report = self.get_object()
		if self.request.user.is_superuser:
			return True
		return False



@login_required(login_url= '/esko_app/login/')
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

class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('esko_app:password_success')



def password_success(request):
	return render(request, 'esko_app/password_reset_done.html')