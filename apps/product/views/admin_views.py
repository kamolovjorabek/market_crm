from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout
from apps.user.models import User
from apps.product.models import Client, Product, Trade, ShopProduct, Basket, Category, \
    ProductPrice
from apps.warehouse.models import Warehouse, InWarehouse, RequestToWarehouse
from django.contrib import messages
from apps.product.forms import CreateShopForm, UpdateShopForm, CreateWarehouseForm, UpdateWarehouseForm, \
    ImportProductWarehouseForm, CreateProductForm, RequestShop
from django.http import HttpResponseRedirect
from django.db.models import Q, Sum, Count
# from apps.warehouse.models import ImportToWarehouse, ProductInWarehouse
# from django.db.models.functions import Coalesce
from apps.user.permisions import LoginRequiredMixin
import datetime
# Create your views here.


class Director(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        page = request.GET.get('page')
        context = {
            'page': 'dashboard'
        }

        match page:
            case None | "dashboard":
                context = {
                    'page': 'dashboard'
                }

            case 'shops':
                q = request.GET.get('q')
                shops = User.objects.filter(role='shop')
                if q:
                    shops = shops.filter(
                        Q(name__icontains=q) | Q(phone__icontains=q) | Q(location__icontains=q)
                    )
                context.update({
                    'q': q,
                    'page': 'shops',
                    'shops': shops
                })

            case 'create.shop':
                context['page'] = 'create.shop'

            case 'update.shop':
                shop_id = request.GET.get('shop.id')
                shop = User.objects.filter(id=shop_id).first()
                context.update({
                    'page': 'update.shop',
                    'shop': shop
                })

            case 'delete.shop':
                shop_id = request.GET.get('shop.id')
                shop = User.objects.filter(id=shop_id).first()
                context.update({
                    'page': 'delete.shop',
                    'shop': shop
                })

            case 'shop':
                shop_id = request.GET.get('shop.id')
                section = request.GET.get('section')
                shop = User.objects.filter(id=shop_id).first()
                context.update({
                    'page': 'shop',
                    'shop': shop,
                    'section': section
                })
                match section:
                    case 'Savdolar':
                        trades = Trade.objects.filter(shop_id=shop_id).select_related('shop', 'product', 'client')
                        context.update({
                            'trades': trades,
                        })
                    case 'Maxsulotlar':
                        products = ShopProduct.objects.filter(shop_id=shop_id).select_related('product', 'shop')
                        context.update({
                            'products': products
                        })
                    case 'Xaridorlar':
                        clients = Client.objects.filter(shop_id=shop_id).select_related('shop')
                        context.update({
                            'clients': clients
                        })
            case 'products':
                q = request.GET.get('q')
                measure = request.GET.get('measure')
                products = Product.objects.filter(category__isnull=False).select_related('category').annotate(
                    basket_is=Count('product_basket__shop', filter=Q(product_basket__shop=request.user))
                )
                print(type(measure))
                if measure:
                    products = products.filter(measure=measure).select_related('category')
                if q:
                    products = products.filter(
                        Q(title__icontains=q)
                    ).select_related('category')
                context.update({
                    'q': q,
                    'page': 'products',
                    'products': products,
                })

            case 'create.product':
                categorys = Category.objects.filter(parent__isnull=True)
                context.update({
                    'page': 'create.product',
                    'categorys': categorys
                })

            case 'delete.product':
                product_id = request.GET.get('product.id')
                product = Product.objects.filter(id=product_id).first()
                product.delete()
                return HttpResponseRedirect('?page=products')
            case 'export':
                product_id = request.GET.get('product.id')
                product = Product.objects.filter(id=product_id).select_related('category').annotate(
                    sell_qty=(Sum('product_qty__qty')),
                    # warehouse_product_price=Coalesce(F('product__discount_price') * F('product_warehouse__qty'), 0)
                ).first()
                warehouse = (Warehouse.objects.filter(shop=2, product_id=product_id).select_related('product', 'shop')
                             .annotate(warehouse_qty=(Sum('qty'))).first())
                date = datetime.date.today()
                context.update({
                    'warehouse': warehouse,
                    'page': 'export',
                    'product': product,
                    'date': date
                })
            case 'basket':
                product_id = request.GET.get('product.id')
                basket = Basket(
                    product_id=product_id,
                    shop=request.user
                )
                basket.save()
                return HttpResponseRedirect('?page=products')

            case 'menu.basket':
                baskets = Basket.objects.filter(shop=request.user).select_related('product', 'shop')
                context.update({
                    'page': 'menu.basket',
                    'baskets': baskets
                })
            case 'delete.basket':
                basket_id = request.GET.get('basket.id')
                basket = Basket.objects.filter(id=basket_id).first()
                basket.delete()
                return HttpResponseRedirect('?page=menu.basket')
            case 'warehouse':
                warehouses = User.objects.filter(role='warehouse')
                context.update({
                    'page': 'warehouse',
                    'warehouses': warehouses
                })

            case 'create.warehouse':
                warehouse_id = request.GET.get('warehouse.id')
                warehouse = User.objects.filter(id=warehouse_id).first()
                context.update({
                    'page': 'create.warehouse',
                    'warehouse': warehouse
                })

            case 'delete.warehouse':
                warehouse_id = request.GET.get('warehouse.id')
                warehouse = User.objects.filter(id=warehouse_id).first()
                warehouse.delete()
                return HttpResponseRedirect('?page=warehouse')

            case 'update.warehouse':
                warehouse_id = request.GET.get('warehouse.id')
                form = request.POST.get('form')
                warehouse = User.objects.filter(id=warehouse_id).first()
                # print(warehouse_id)
                # print(warehouse)
                context.update({
                    'page': 'update.warehouse',
                    'warehouse': warehouse,
                    'form': form
                })

            case 'warehouse.product.list':
                warehouse_id = request.GET.get('warehouse.id')
                import_warehouse_products = Warehouse.objects.filter(shop_id=warehouse_id).select_related('product', 'shop').order_by('-id')
                warehouse = User.objects.filter(role='warehouse', id=warehouse_id).first()
                context.update({
                    'warehouse': warehouse,
                    'page': 'warehouse.product.list',
                    'import_warehouse_products': import_warehouse_products
                })
            case 'import.product.warehouse':
                warehouse_id = request.GET.get('warehouse.id')
                warehouse = User.objects.filter(role='warehouse', id=warehouse_id).first()
                products = Product.objects.all()
                context.update({
                    'warehouse': warehouse,
                    'page': 'import.product.warehouse',
                    'products': products
                })
            case 'product.in.warehouse':
                warehouse_id = request.GET.get('warehouse.id')
                warehouse = User.objects.filter(role='warehouse', id=warehouse_id).first()
                products = InWarehouse.objects.filter(shop=warehouse_id).order_by('-id')
                print(products)
                context.update({
                    'page': 'product.in.warehouse',
                    'products': products,
                    'warehouse': warehouse
                })
            case 'request.shop':
                warehouse_id = request.GET.get('warehouse.id')
                warehouse = User.objects.filter(role='warehouse', id=warehouse_id).first()
                request_products = RequestToWarehouse.objects.filter(warehouse_id=warehouse_id, status='new').select_related(
                    'shop', 'warehouse', 'product')
                context.update({
                    'page': 'request.shop',
                    'request_products': request_products,
                    'warehouse': warehouse
                })
            case 'form.request.shop':
                warehouse_id = request.GET.get('warehouse.id')
                warehouse = User.objects.filter(role='warehouse', id=warehouse_id).first()
                warehouse_id = request.GET.get('warehouse.id')
                request_product = RequestToWarehouse.objects.filter(warehouse_id=warehouse_id, status='new').first()
                context.update({
                    'page': 'form.request.shop',
                    'request_product': request_product,
                    'warehouse': warehouse
                })
            case 'sent.shop':
                warehouse = request.GET.get('warehouse.id')
                request_product = request.GET.get('request_product')
                form = RequestShop(request.GET)
                if form.is_valid():
                    obj = RequestToWarehouse.objects.filter(
                        id=request_product
                    ).first()
                    obj.status = 'accepted'
                    in_warehouse = InWarehouse.objects.filter(product_id=obj.product.id).first()
                    in_warehouse.qty -= obj.qty
                    in_warehouse.save()
                    obj.save()
                    form.save()
                    return HttpResponseRedirect(f'?page=request.shop&warehouse.id={warehouse}')
                else:
                    print(form.errors)
        return render(request, 'index.html', context)

    @staticmethod
    def post(request):
        post = request.POST.get('post')
        context = {
        }
        match post:
            case 'logout':
                logout(request)
                return redirect('dashboard')

            case 'create.shop':
                form = CreateShopForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('?page=shops')
                else:
                    print(form)
                    context.update({
                        'page': 'create.shop',
                        'form': form
                    })
                    return render(request, 'index.html', context)

            case 'update.shop':
                shop_id = request.POST.get('shop.id')
                shop = User.objects.filter(id=shop_id).first()
                form = UpdateShopForm(request.POST, instance=shop)
                if form.is_valid():
                    form.save()
                return HttpResponseRedirect('?page=shops')
            case 'delete.shop':
                shop_id = request.POST.get('shop.id')
                shop = User.objects.filter(id=shop_id).first()
                shop.delete()
                return HttpResponseRedirect('?page=shops')

            case 'create.warehouse':
                form = CreateWarehouseForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('?page=warehouse')

            case 'update.warehouse':
                warehouse_id = request.POST.get('warehouse.id')
                warehouse = User.objects.filter(id=warehouse_id).first()
                form = UpdateWarehouseForm(request.POST, instance=warehouse)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('?page=warehouse')
                else:
                    context = {
                        'page': 'update.warehouse',
                        'warehouse': warehouse,
                        'form': form
                    }
                    return render(request, 'index.html', context)
            case 'import.product.warehouse':
                shop = request.POST.get('shop')
                form = ImportProductWarehouseForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(f'?page=warehouse.product.list&warehouse.id={shop}')
                else:
                    print(form.errors)

            case 'create.product':
                form = CreateProductForm(request.POST)
                if form.is_valid():
                    obj = form.save()
                    ProductPrice.objects.create(
                        product=obj,
                        price=request.POST.get('price'),
                        discount=request.POST.get('discount')
                    )
                    return HttpResponseRedirect('?page=products')
                else:
                    print(form.errors)
