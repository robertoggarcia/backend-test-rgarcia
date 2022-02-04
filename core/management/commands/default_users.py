from django.core.management import BaseCommand
from django.contrib.auth.models import Permission, User, Group
from django.db import IntegrityError

MODELS = ['menu', 'menu option', 'order']
ROLES = {
    'chef': {
        'menu': ['add', 'change', 'view'],
        'menu option': ['add', 'view'],
        'order': ['view'],
    },
    'employee': {
        'menu option': [],
        'menu': ['view'],
        'order': ['add', 'view']
    }
}


class Command(BaseCommand):
    help = 'Create default users and set groups and permissions'

    def handle(self, *args, **options):
        for role, values in ROLES.items():
            try:
                user = User.objects.create_user(role, f'{role}@cornershop.com',
                                                'Corner$h0p')
            except IntegrityError:
                user = User.objects.get(username=role)

            for model, permissions in values.items():
                group, _ = Group.objects.get_or_create(name=f"{role}s")
                user.groups.add(group.pk)
                for permission in permissions:

                    name = 'Can {} {}'.format(permission, model)

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        continue
                    group.permissions.add(model_add_perm)

        self.stdout.write(self.style.SUCCESS('Successfully created'))
