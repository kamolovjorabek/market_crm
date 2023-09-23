from django.shortcuts import render, redirect
from django.views.generic import View

from apps.product.forms import TradeForm
from apps.product.models import Trade, ShopProduct, ProductPrice
from apps.user.models import User
from apps.product.models import Product
from apps.user.permisions import LoginRequiredMixin
from apps.warehouse.forms import RequestToWarehouseForm
from apps.warehouse.models import RequestToWarehouse
from django.http import HttpResponseRedirect
from django.db.models import F, When, Case, Subquery, OuterRef, Sum
from django.db.models.fields import IntegerField
# Create your views here.


class Shop(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        page = request.GET.get('page')
        context = {
            'page': page,
        }
        match page:
            case None | 'dashboard':
                trade = ShopProduct.objects.filter(shop_id=request.user.id).select_related('shop', 'product').annotate(
                    sold_qty=
                        Trade.objects.filter(
                            shop_id=OuterRef('shop_id'),
                            product_id=OuterRef('product_id')
                        ).values('product_id').annotate(t=Sum('qty')).values('t')
                )
                # trade = Trade.objects.filter(shop_id=request.user.id).select_related('shop', 'product').annotate(
                #     product_name=F('product__title'),
                #     sold_qty=Sum(
                #             ShopProduct.objects.filter(shop_id=OuterRef('shop_id'),
                #                                        product_id=OuterRef('product_id')).values('qty')
                #     )
                # )

                print(trade.values('sold_qty'))
                # print(trade)
                context = {
                    'page': 'dashboard',
                }
            case 'trade':
                measure = request.GET.get('measure')
                trades = Trade.objects.filter(shop=request.user.id).select_related('shop', 'product', 'client').annotate(
                    category=F('product__category__title')
                ).order_by('-id')[:10]
                if measure:
                    trades = trades.filter(product__measure=measure)
                shop_products = ShopProduct.objects.annotate(
                    product_title=F('product__title'),
                    product_price=Subquery(ProductPrice.objects.filter(product_id=OuterRef('product_id')).values('price')[:1]
                ))
                context.update({
                    'shop_products': shop_products,
                    'trades': trades
                })
            case 'request.warehouse.product.list':
                status = request.GET.get('status')
                request_products = (RequestToWarehouse.objects.select_related
                                    ('shop', 'warehouse', 'product').filter(shop_id=request.user.id)).annotate(
                    category_name=F('product__category__title')
                )
                if status:
                    request_products = request_products.filter(status=status)
                context.update({
                    'request_products': request_products
                })
            case 'request.to.warehouse':
                warehouses = User.objects.filter(role='warehouse')
                products = Product.objects.all()
                context.update({
                    'warehouses': warehouses,
                    'products': products
                })
            case 'shop.products':
                products = ShopProduct.objects.filter(shop=request.user.id).select_related('product', 'shop').annotate(
                    category=F('product__category__title')
                )
                context.update({
                    'products': products
                })
            case 'confirmed.product':
                request_product = request.GET.get('request_product')
                request_products = RequestToWarehouse.objects.filter(id=int(request_product)).first()
                print(request_products)
                context.update({
                    'request_products': request_products
                })
            case 'confirmed.shop':
                request_product_id = request.GET.get('request_product_id')
                qty = request.GET.get('qty')
                request_product = request.GET.get('request_product_product')
                request_warehouse = RequestToWarehouse.objects.filter(id=request_product_id).first()
                if request_warehouse.status == 'accepted':
                    shop_product, _ = ShopProduct.objects.get_or_create(shop_id=request.user.id, product_id=request_product)
                    request_warehouse.status = 'confirmed'
                    request_warehouse.save()
                    shop_product.qty += int(qty)
                    shop_product.save()
                    return HttpResponseRedirect("?page=request.warehouse.product.list")
                else:
                    return HttpResponseRedirect("?page=request.warehouse.product.list")
        return render(request, 'shop_index.html', context)

    @staticmethod
    def post(request):
        post = request.POST.get('post')

        match post:
            case 'request.to.warehouse':
                form = RequestToWarehouseForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.shop = request.user
                    obj.save()
                    return HttpResponseRedirect('?page=request.warehouse.product.list')
                else:
                    print(form.errors)
            case 'trade':
                form = TradeForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    if request.POST.get('price'):
                        obj.sold_price = request.POST.get('price')
                    else:
                        obj.sold_price = obj.product.price.price
                    shop_product = ShopProduct.objects.filter(product_id=request.POST.get('product')).first()
                    shop_product.qty -= int(request.POST.get('qty'))
                    shop_product.save()
                    obj.shop = request.user
                    obj.save()
                    return HttpResponseRedirect("?page=trade")
