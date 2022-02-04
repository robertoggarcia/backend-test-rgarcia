from django.contrib.auth.models import User
from django.db import models
from core.models import BaseModel
from menus.models import Menu, MenuOption


class Order(BaseModel):
    """
    Stores a single order entry, related to :model:`menus.Menu`,
    :model:`menus.MenuOption` and :model:`auth.User`.
    """
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(MenuOption, on_delete=models.SET_NULL,
                               null=True)
    order_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customization = models.CharField(max_length=300, null=True)
