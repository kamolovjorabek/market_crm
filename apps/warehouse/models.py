from django.db import models

from apps.product.models import Product
from apps.user.models import User
from apps.warehouse.enums import RequestStatus


class Warehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_warehouse')
    qty = models.PositiveIntegerField()
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InWarehouse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(default=0)
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.CharField(max_length=100, blank=True, null=True)


class RequestToWarehouse(models.Model):
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='shop_request_warehouse')
    warehouse = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='warehouse_request')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_request')
    qty = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=RequestStatus.choices(), default=RequestStatus.choices()[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def warehouse_qty(self):
        qty = InWarehouse.objects.filter(product_id=self.product.id, shop_id=self.warehouse.id).first()
        return qty
