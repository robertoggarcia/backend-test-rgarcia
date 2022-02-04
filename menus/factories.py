import factory
import datetime

from menus.models import MenuOption, Menu


class MenuOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MenuOption

    name = factory.Sequence(lambda n: 'Option%d' % n)


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    description = factory.Faker('catch_phrase')
    date = factory.LazyFunction(datetime.datetime.now)
