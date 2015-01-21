"""
player/forms.py
"""
from django.forms import ModelForm, RadioSelect
from inventory.models import Item
from . import models


class CreateCharacter(ModelForm):
    """
    Create a character
    """

    class Meta:
        fields = (
            'name',
            'category',
            'notes',
            )
        model = models.PlayerCharacter


class UpdateCharacter(ModelForm):
    """
    Let user modify name, notes, and auto-act values of a character
    """

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


class Settings(ModelForm):
    """
    Account-wide settings.
    """

    class Meta:
        fields = (
            'auto_loot',
            'fov',
            'fps',
            )
        model = models.Config
        widgets = {
            'fov': RadioSelect(),
            'fps': RadioSelect(),
            }
