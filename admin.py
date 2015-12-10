from django.contrib import admin
from .models import restaurant, comments
from .forms import restaurantRegistrationForm

# Restaurant registration admin view setting
class restaurantRegistrationAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'user', 'location', 'typeOfFood', 'rating', 'timestamp']

# Restaurant comment admin view setting
class restaurantCommentAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'user', 'timestamp', 'updated']

# Registered the change
admin.site.register(restaurant, restaurantRegistrationAdmin)
admin.site.register(comments, restaurantCommentAdmin)