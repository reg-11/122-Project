from django.urls import path, include

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
	path('profile/', views.profile, name='profile'),

]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)