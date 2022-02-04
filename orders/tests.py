from unittest import mock

from django.urls import reverse
from django.utils import timezone

from core.tests import BaseTest
from menus.factories import MenuFactory, MenuOptionFactory
from orders.models import Order

D_FORMAT = "%Y-%m-%d %H:%M:%S"


class OrderTest(BaseTest):

    @mock.patch('orders.views.localtime')
    def test_create_order(self, m_localtime):
        s_time = '2022-01-01 10:00:00'
        m_localtime.return_value = timezone.datetime.strptime(s_time, D_FORMAT)
        menu = MenuFactory.create(date='2022-01-01')
        option = MenuOptionFactory.create()
        data = {
            'option': option.id,
            'customization': 'Test',
            'menu': menu.id,
            'order_by': self.employee.id
        }

        self.client.force_login(self.employee)
        response = self.client.post(
            reverse('menu-detail', kwargs={'pk': menu.id}),
            data=data
        )

        self.assertRedirects(response, f'/menus/{menu.id}/')
        self.assertEqual(
            Order.objects.filter(
                order_by=self.employee, option=option.id).count(), 1
        )

    @mock.patch('orders.views.localtime')
    def test_create_order_fail(self, m_localtime):
        s_time = '2022-01-01 11:00:00'
        m_localtime.return_value = timezone.datetime.strptime(s_time, D_FORMAT)

        menu = MenuFactory.create(date='2022-01-01')
        option = MenuOptionFactory.create()
        data = {
            'option': option.id,
            'customization': 'Test',
            'menu': menu.id,
            'order_by': self.employee.id
        }

        self.client.force_login(self.employee)
        response = self.client.post(
            reverse('menu-detail', kwargs={'pk': menu.id}),
            data=data
        )

        self.assertIn('It is not possible to order for this menu!',
                      str(response.content))
        self.assertEqual(
            Order.objects.filter(
                order_by=self.employee, option=option).count(), 0
        )
