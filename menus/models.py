from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel


class MenuOption(BaseModel):
    """
    Stores a single menu option entry
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Menu(BaseModel):
    """
    Stores a single menu entry, related to :model:`menus.MenuOption` and
    :model:`auth.User`.
    """
    description = models.CharField(max_length=300)
    options = models.ManyToManyField(MenuOption, related_name='menus')
    date = models.DateField(unique=True)
    created_by = models.ForeignKey(
        User,
        related_name='menus',
        on_delete=models.SET_NULL,
        null=True
    )
