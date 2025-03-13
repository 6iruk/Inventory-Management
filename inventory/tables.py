import django_tables2 as tables
from django.utils.html import format_html
from inventory.models import *

class MaterialTable(tables.Table):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity', 'buying_price', 'selling_price']

class ManagerMaterialTable(tables.Table):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity']

class CashierMaterialTable(tables.Table):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity', 'selling_price']


class SaleTable(tables.Table):
    class Meta:
        model = Sale
        fields = ['material', 'quantity', 'sales_date', 'notes']


class EmployeeTable(tables.Table):
    class Meta:
        model = Employee
        fields = ['name', 'phone_number','notes', 'is_active']


class OrderTable(tables.Table):
    class Meta:
        model = Order
        fields = ['employee', 'material','quantity', 'order_date', 'notes']
