from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from menus.forms import CreateMenuForm
from menus.models import Menu
from orders.forms import CreateOrderForm
from orders.models import Order
from orders.views import OrderFormView


class MenuCreateView(CreateView):
    """
    Display create new menu form :model:`menus.Menu`.

    **Template:**

    :template:`menus/menu_form.html`
    """
    model = Menu
    form_class = CreateMenuForm
    success_url = '/menus/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class MenuUpdateView(UpdateView):
    """
    Update view :model:`menus.Menu`.

    **Template:**

    :template:`menus/menu_update_form.html`
    """
    model = Menu
    fields = ['description', 'options', 'date']
    template_name_suffix = '_update_form'
    success_url = '/menus/'


class MenuListView(ListView):
    """
    List menu items :model:`menus.Menu`.

    **Template:**

    :template:`menus/menu_list.html`
    """
    model = Menu
    ordering = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            return context

        is_employee = self.request.user.groups.filter(name='employees').exists()
        context["is_employee"] = is_employee
        return context


class MenuRetrieveView(SuccessMessageMixin, DetailView):
    """
    Display menu detail  and order form :model:`menus.Menu`.

    **Template:**

    :template:`menus/menu_detail.html`
    """
    model = Menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            return context

        is_employee = self.request.user.groups.filter(name='employees').exists()
        menu = self.get_object()
        context["is_employee"] = is_employee

        if not is_employee:
            orders = Order.objects.filter(menu=menu)
            context['orders'] = orders

        if is_employee:
            order = Order.objects.filter(menu=menu,
                                         order_by=self.request.user)

            if not order.exists():
                form = CreateOrderForm()
                form.fields['menu'].initial = menu.pk
                form.fields['order_by'].initial = self.request.user.pk
                form.fields['option'].queryset = menu.options.all()
                context['form'] = form
            else:
                context['order'] = order.last()
        return context


class MenuDetailView(View):
    """
    Display menu detail :model:`menus.Menu`.
    **Context**
    ``orders``
        A queryset of :model:`menus.Menu`. Only for chef users.
    ``order``
        An instance of :model:`menus.Menu`. Ifs a employee user have one.
    ``form``
        A create order form.
    **Template:**
    :template:`menus/menu_form.html`
    """

    def get(self, request, *args, **kwargs):
        view = MenuRetrieveView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = OrderFormView.as_view()
        return view(request, *args, **kwargs)
