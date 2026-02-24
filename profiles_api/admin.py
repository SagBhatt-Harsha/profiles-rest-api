from django.contrib import admin
from . import models

# Register your models to the Admin Site here.

admin.site.register(models.UserProfile) #* Registering UserProfile Model to the Django admin.

admin.site.register(models.ProfileFeedItems) #* Registering ProfileFeedItems Model to the Django admin.