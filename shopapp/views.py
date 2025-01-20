from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from timeit import default_timer

from .forms import ProductForm, GroupForm
from shopapp.models import Product, Order
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        products = [
            ('телефон', '1000'),
            ('планшет!', '2000'),
            ('колонка', '500'),
        ]

        dict1 = {
            'time_running': default_timer(),
            'goods': products,
        }

        return render(request, 'shopapp/index.html', context=dict1)


def shop_index(request: HttpRequest):

    products = [
        ('телефон', '1000'),
        ('планшет!', '2000'),
        ('колонка', '500'),
    ]

    dict1 = {
        'time_running': default_timer(),
        'goods': products,
    }

    return render(request,'shopapp/index.html', context=dict1)


def group_list(request: HttpRequest):
    context={
        'groups': Group.objects.prefetch_related('permissions').all()
    }
    return render(request, 'shopapp/group-list.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all()
        }
        return render(request, 'shopapp/group-list.html', context=context)


    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'shopapp/products-list.html', context=context)


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['products'] = Product.objects.all()
    #    return context



#class ProductDetailView(View):
#    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#        #product = Product.objects.get(pk=pk)
#        product = get_object_or_404(Product, pk=pk)
#
#        context = {
#            'product': product
#        }
#        return render(request, 'shopapp/products-details.html', context=context)


class ProductDetailView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'


def create_product(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():

            form.save()

            url = reverse('shopapp:products_list')
            return redirect(url)
    else:
        form = ProductForm()

    context={
        'form': form
    }
    return render(request, 'shopapp/product_form.html', context=context)


class ProductCreateView(CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all(),
    }
    return render(request, 'shopapp/order_list.html', context=context)


class OrderListView(ListView):
    #model = Order
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )


class OrderDetailView(DetailView):
    #model = Order
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )