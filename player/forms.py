"""
player/forms.py
"""
from django.forms import ModelForm
from mobile import models


class CreateCharacter(ModelForm):
    class Meta:
        fields = (
            'name',
            'species',
            'gender',
            'notes',
            )
        model = models.PlayerCharacter


class UpdateCharacter(ModelForm):
    class Meta:
        fields = (
            'name',
            'notes',
            )
        model = models.PlayerCharacter
