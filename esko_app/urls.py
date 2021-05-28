from django.urls import path, include

from .views import PostListView, PostDetailView,PostCreateView, PostUpdateView, PostDeleteView, AddCommentView
from . import views


from django.conf import settings
from django.conf.urls.static import static

app_name = 'esko_app'
urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup, name='signup'),
	path('login/', views.loginPage, name='login'),
	path('home/', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('logout/', views.logoutUser, name='logout'),
	path('profile/', PostListView.as_view(), name='profile'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('profileSettings/', views.profileSettings, name='profileSettings'),
	path('like/<int:pk>/',views.LikeView, name='like_post'),
	path('post/<int:pk>/comment', AddCommentView.as_view(), name='add_comment'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)