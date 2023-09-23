from django import forms
from apps.warehouse.models import RequestToWarehouse


class RequestToWarehouseForm(forms.ModelForm):
    class Meta:
        model = RequestToWarehouse
        fields = ('warehouse', 'product', 'qty')
