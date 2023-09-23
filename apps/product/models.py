from django.db import models
from apps.user.models import User
from apps.product.enums import Measure, WarehouseStatus
# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True , blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    measure = models.CharField(max_length=10, choices=Measure.choices())
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def price(self):
        return ProductPrice.objects.filter(product_id=self.id).last()

    def __str__(self):
        return self.title


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    discount = models.PositiveIntegerField(default=0)

    def discount_price(self):
        return self.price - ((self.price * self.discount) / 100)


class ShopProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='filter_product')
    qty = models.PositiveBigIntegerField(default=0)
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_basket')
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Trade(models.Model):
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_qty')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    sold_price = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class AcceptedToShop(models.Model):
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='shop_request_history')
    warehouse = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='warehouse_request_history')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    request_qty = models.IntegerField(default=0)
    sent_qty = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=WarehouseStatus.choices(), default=WarehouseStatus.choices()[0][0])
    created_at = models.DateTimeField(auto_now_add=True)

