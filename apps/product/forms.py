from django import forms
# from django.forms import ModelForm
from django.core.exceptions import ValidationError
from apps.product.models import Product, AcceptedToShop, Trade
from apps.warehouse.models import Warehouse, InWarehouse, RequestToWarehouse
from apps.user.models import User


class CreateShopForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('name', 'phone', 'location')

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if (password1 and password2) and (password1 != password2):
            self.add_error('password1', ValidationError('Paasword error', 'passwd_mismatch'))
        if not self.errors:
            return True
        return False

    def save(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        name = self.cleaned_data.get("name")
        phone = self.cleaned_data.get("phone")
        location = self.cleaned_data.get("location")

        user = self.Meta.model.objects.create_user(
            name=name,
            location=location,
            phone=phone,
            role='shop',
            password=password1
        )
        user.save()


class UpdateShopForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'phone', 'location')


class CreateWarehouseForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('name', 'phone', 'location')

    def save(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if (password1 and password2) and (password1 != password2):
            raise forms.ValidationError('Paasword error')

        name = self.cleaned_data.get("name")
        phone = self.cleaned_data.get("phone")
        location = self.cleaned_data.get("location")

        user = self.Meta.model.objects.create_user(
            name=name,
            location=location,
            phone=phone,
            role='warehouse',
            password=password1
        )
        user.save()


class UpdateWarehouseForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('name', 'phone', 'location')

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if (password1 and password2) and (password1 != password2):
            self.add_error('password2', ValidationError('Password error', 'passwd_mismatch'))
        if not self.errors:
            return True
        return False

    def save(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            self.instance.set_password(password1)
        self.instance.save()
        return self.instance


class ImportProductWarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ('product', 'qty', 'shop')

    def save(self, *args, **kwargs):
        in_warehouse, _ = InWarehouse.objects.get_or_create(
            shop=self.cleaned_data.get('shop'),
            product=self.cleaned_data.get('product')
        )
        in_warehouse.qty += self.cleaned_data.get('qty')
        in_warehouse.save()
        self.instance.save()


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'category', 'measure')


class RequestShop(forms.ModelForm):
    class Meta:
        model = AcceptedToShop
        fields = ('shop', 'warehouse', 'product', 'request_qty', 'sent_qty')


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ('product', 'qty')
