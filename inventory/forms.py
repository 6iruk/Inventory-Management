from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from inventory.models import *
from django.contrib.admin.widgets import AdminDateWidget

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity', 'buying_price', 'selling_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('material_type', css_class='form-group col-md-4 mb-0'),
                Column('material_code', css_class='form-group col-md-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column('stock_quantity', css_class='form-group col-md-4 mb-0'),
                Column('buying_price', css_class='form-group col-md-4 mb-0'),
                Column('selling_price', css_class='form-group col-md-4 mb-0'),
                Column('description', css_class='form-group col-md-4 mb-0'),
                css_class='row mb-4'
            ),
            Submit('submit', 'ADD')
        )

class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['material', 'quantity', 'sales_date', 'notes']
        widgets = {
            'sales_date':forms.DateInput(attrs={'type':'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('material', css_class='form-group col-md-4 mb-0'),
                Column('quantity', css_class='form-group col-md-4 mb-0'),
                Column('sales_date', css_class='form-group col-md-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column('notes', css_class='form-group col-md-4 mb-0'),
                css_class='row mb-4'
            ),
            Submit('submit', 'ADD')
        )

    def clean(self):
        super().clean()
        quantity = self.cleaned_data.get("quantity")
        material = self.cleaned_data.get("material")
        print(material.stock_quantity)
        if material.stock_quantity < quantity:
            raise ValidationError(
                f'Only {material.stock_quantity} left'
            )

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone_number','notes', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('phone_number', css_class='form-group col-md-4 mb-0'),
                Column('notes', css_class='form-group col-md-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column('is_active', css_class='form-group col-md-4 mb-0'),
                css_class='row mb-4'
            ),
            Submit('submit', 'ADD')
        )

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['employee', 'material','quantity', 'order_date', 'notes']
        widgets = {
            'order_date':forms.DateInput(attrs={'type':'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='form-group col-md-4 mb-0'),
                Column('material', css_class='form-group col-md-4 mb-0'),
                Column('quantity', css_class='form-group col-md-4 mb-0'),
                css_class='row'
            ),
            Row(
                Column('order_date', css_class='form-group col-md-4 mb-0'),
                Column('notes', css_class='form-group col-md-4 mb-0'),
                css_class='row mb-4'
            ),
            Submit('submit', 'ADD')
        )

    def clean(self):
        super().clean()
        quantity = self.cleaned_data.get("quantity")
        material = self.cleaned_data.get("material")
        
        if material.stock_quantity < quantity:
            raise ValidationError(
                f'Only {material.stock_quantity} left'
            )