from django.contrib import admin

from . import models
admin.site.register(models.Gender)
admin.site.register(models.Species)
admin.site.register(models.PlayerCharacter)
admin.site.register(models.NonPlayerCharacter)

