from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import localtime
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from backend_test.settings import CAN_ORDER_THRESHOLD
from menus.models import Menu
from orders.forms import CreateOrderForm

DATE_FORMAT = '%Y-%m-%d'


def same_date(date_1, date_2):
    """Validate if two dates are the same with DATE_FORMAT"""
    return date_1.strftime(DATE_FORMAT) == date_2.strftime(DATE_FORMAT)


class OrderFormView(SingleObjectMixin, FormView):
    """
    Create a single :model:`orders.Order` form view.
    """
    form_class = CreateOrderForm
    model = Menu
    template_name = 'menus/menu_detail.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()

        local_time = localtime()
        if local_time.hour >= CAN_ORDER_THRESHOLD or not same_date(
                local_time, self.object.date):
            return render(
                request,
                'orders/order_not_allowed.html',
                {'menu': self.object.pk}
            )

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.order_by = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('menu-detail', kwargs={'pk': self.object.pk})
