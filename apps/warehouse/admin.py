from django.contrib import admin
from apps.warehouse.models import Warehouse, InWarehouse, RequestToWarehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'shop', 'created_at')


@admin.register(InWarehouse)
class InWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'shop', 'created_at')


@admin.register(RequestToWarehouse)
class RequestToWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'warehouse', 'product', 'status', 'created_at', 'update_at')
