from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
	year_level = models.CharField(max_length=30, blank=True)
	phone_number = models.IntegerField(null=True,blank=True)
	sns_account = models.URLField(max_length = 200,blank=True)
	bio = models.CharField(max_length=200, blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'

# class User(models.Model):
	
# 	user_id = models.AutoField(primary_key=True)
# 	email = models.CharField(max_length=50,unique=True)
# 	password = models.CharField(max_length=30,unique=True)
# 	username = models.CharField(max_length=30, blank=True,unique=True)
# 	year_level = models.CharField(max_length=30, blank=True)
# 	phone_number = models.IntegerField(blank=True)
# 	sns_account = models.URLField(max_length = 200)
# 	bio = models.CharField(max_length=200, blank=True)

# 	def __str__(self):
# 		return self.username, self.year_level, self.phone_number, self.sns_account,self.bio

class Post(models.Model):
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.CharField(max_length=30)
	description = models.CharField(max_length=200)
	tags = models.CharField(max_length=100)
	image = models.ImageField(null=True,blank=True)
	date = models.DateField()

	def __str__(self):
		return self.category, self.description, self.tags


