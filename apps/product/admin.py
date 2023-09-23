from django.contrib import admin
from .models import (
    Product,
    Category,
    Client,
    Trade,
    ShopProduct,
    Basket,
    ProductPrice,
    AcceptedToShop
)
# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'shop', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at')


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'shop')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'shop', 'created_at')


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'discount')


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'product', 'client', 'sold_price', 'qty', 'created_at')


@admin.register(AcceptedToShop)
class AcceptedToShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'warehouse', 'product', 'request_qty', 'sent_qty', 'status', 'created_at')



