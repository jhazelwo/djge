from django.contrib import admin
from . import models
admin.site.register(models.Config)
admin.site.register(models.PlayerCharacter)
admin.site.register(models.Journal)
