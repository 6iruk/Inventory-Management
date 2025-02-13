import django_tables2 as tables
from django.utils.html import format_html
from inventory.models import *

class MaterialTable(tables.Table):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity', 'buying_price', 'unit_price']

class ManagerMaterialTable(tables.Table):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity']

class CashierMaterialTable(tables.Table):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity', 'unit_price']