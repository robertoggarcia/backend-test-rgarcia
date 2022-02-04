from datetime import datetime, timedelta
from unittest import mock

from django.urls import reverse

from core.tests import BaseTest
from menus.factories import MenuFactory, MenuOptionFactory
from menus.forms import CreateMenuForm
from menus.models import MenuOption, Menu
from menus.tasks import send_menu


class MenuTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.menu_option = MenuOption.objects.create(name='Testing')

    def test_create_menu(self):
        data = {
            'description': 'Testing',
            'options': [str(self.menu_option.id)],
            'date': '2022-01-01'
        }

        self.client.force_login(self.chef)
        response = self.client.post(reverse('menu-add'), data=data)

        self.assertRedirects(response, '/menus/')
        self.assertEqual(
            Menu.objects.filter(description=data['description']).count(), 1
        )

    def test_duplicated_menu(self):
        data = {
            'description': 'Testing',
            'options': [str(self.menu_option.id)],
            'date': '2022-01-02'
        }
        MenuFactory.create(date=data['date'])

        form = CreateMenuForm(data=data)

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['date'][0], 'Menu with this Date already exists.')

    @mock.patch('menus.tasks.send_slack_message')
    def test_send_menu_task(self, m_send_slack_message):
        menu = MenuFactory.create()

        task_menu = send_menu()

        self.assertEqual(menu.description, task_menu.description)
        self.assertTrue(m_send_slack_message.called)

    def test_send_menu_task_fail(self):
        MenuFactory.create(
            date=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        )

        task_menu = send_menu()

        self.assertFalse(task_menu)

    def test_edit_menu(self):
        menu = MenuFactory.create()
        menu_option = MenuOptionFactory.create()

        data = {
            'description': 'Testing',
            'options': [str(menu_option.id)],
            'date': '2022-01-01'
        }

        self.client.force_login(self.chef)
        response = self.client.post(
            reverse('menu-update', kwargs={'pk': menu.id}), data=data
        )

        self.assertRedirects(response, '/menus/')
        menu_up = Menu.objects.get(id=menu.id)
        self.assertEqual(len(menu_up.options.all()), 1)

    def test_edit_menu_as_employee(self):
        menu = MenuFactory.create()

        self.client.force_login(self.employee)
        response = self.client.post(
            reverse('menu-update', kwargs={'pk': menu.id}), data={}
        )

        self.assertRedirects(response,
                             f'/accounts/login/?next=/menus/update/{menu.id}/')
