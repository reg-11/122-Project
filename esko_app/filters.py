from django import forms
import django_filters

from .models import Post, Category

class PostFilter(django_filters.FilterSet):
	sell = 'sell'
	services = 'services/rent'
	swap = 'swap'
	find = 'find'

	category_choices = [
		(sell, sell),
		(services, services),
		(swap, swap),
		(find, find),
	]
	
	#category = django_filters.ChoiceFilter(choices=Post.objects.all())
	#category = django_filters.ChoiceFilter(choices=category_choices, widget=forms.Select(attrs={'class':'form-select', 'style':'background:$primary'}))
	class Meta:
		model = Post
		fields = [
			'category',
		]
		