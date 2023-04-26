from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


# главная страница


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


# класс продуктов с категориями и пагинацией
class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


# Добавление в корзину


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product).first()

    if not baskets:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = Basket.objects.get(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Удаление из корзины
@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


""" @staticmethod
def _get_items_count(response):
    paginator = response.context_data.get('paginator') - # универсальный метод

    return paginator.per_page if paginator else None


def _get_product_list(self, response, filter_args: dict = None) -> list:
    if filter_args:
        product_list = Product.objects.filter(**filter_args)
    else:
        product_list = Product.objects.all()

    items_count = self._get_items_count(response)
    if items_count:
        product_list = product_list[:items_count]

    return list(product_list) """
