"""
player/forms.py
"""
from django.forms import ModelForm, RadioSelect
from . import models


class CreateCharacter(ModelForm):
    class Meta:
        fields = (
            'name',
            'category',
            'notes',
            )
        model = models.PlayerCharacter


class UpdateCharacter(ModelForm):
    class Meta:
        fields = (
            'name',
            'notes',
            'c01',
            'c02',
            'c03',
            'c04',
            'c05',
            'c06',
            'c07',
            'c08',
            )
        model = models.PlayerCharacter
        widgets = {
            'c01': RadioSelect(),
            'c02': RadioSelect(),
            'c03': RadioSelect(),
            'c04': RadioSelect(),
            'c05': RadioSelect(),
            'c06': RadioSelect(),
            'c07': RadioSelect(),
            'c08': RadioSelect(),
        }
