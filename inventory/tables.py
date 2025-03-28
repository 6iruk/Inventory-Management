import django_tables2 as tables
from django.utils.html import format_html
from inventory.models import *

    
class MaterialTable(tables.Table):
    update = tables.TemplateColumn(
    '<a class="btn btn-success" href="/material?id={{ record.id }}">Update</a><a class="btn btn-danger mt-2" onclick="deleteModal(\'/material?\', {{ record.id }})"  data-bs-toggle="modal" data-bs-target="#deleteModal">Delete</a>',
        verbose_name='',
        orderable=False,
        attrs={
            "td": {"style": "max-width: min-content;"}
        }
    )

    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'purchase_date', 'purchase_quantity', 'stock_quantity', 'buying_price', 'selling_price']

class ManagerMaterialTable(tables.Table):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity']

class CashierMaterialTable(tables.Table):
    class Meta:
        model = Material
        fields = ['name', 'material_type', 'material_code', 'description', 'stock_quantity', 'selling_price']


class SaleTable(tables.Table):
    update = tables.TemplateColumn(
    '<a class="btn btn-success" href="/sale?id={{ record.id }}">Update</a><a class="btn btn-danger mt-2" onclick="deleteModal(\'/sale?\', {{ record.id }})"  data-bs-toggle="modal" data-bs-target="#deleteModal">Delete</a>',
        verbose_name='',
        orderable=False,
        attrs={
            "td": {"style": "max-width: min-content;"}
        }
    )

    class Meta:
        model = Sale
        fields = ['material', 'quantity', 'price', 'sales_date', 'user__username', 'notes']

class CashierSaleTable(tables.Table):
    class Meta:
        model = Sale
        fields = ['material', 'quantity', 'price', 'sales_date', 'notes']

class EmployeeTable(tables.Table):
    update = tables.TemplateColumn(
    '<a class="btn btn-success" href="/employee?id={{ record.id }}">Update</a><a class="btn btn-danger mt-2" onclick="deleteModal(\'/employee?\', {{ record.id }})"  data-bs-toggle="modal" data-bs-target="#deleteModal">Delete</a>',
        verbose_name='',
        orderable=False,
        attrs={
            "td": {"style": "max-width: min-content;"}
        }
    )

    class Meta:
        model = Employee
        fields = ['id', 'name', 'phone_number','notes', 'is_active']


class OrderTable(tables.Table):
    update = tables.TemplateColumn(
    '<a class="btn btn-success" href="/order?id={{ record.id }}">Update</a><a class="btn btn-danger mt-2" onclick="deleteModal(\'/order?\', {{ record.id }})"  data-bs-toggle="modal" data-bs-target="#deleteModal">Delete</a>',
        verbose_name='',
        orderable=False,
        attrs={
            "td": {"style": "max-width: min-content;"}
        }
    )

    class Meta:
        model = Order
        fields = ['employee', 'material','quantity', 'order_date', 'user__username', 'notes']

class ManagerOrderTable(tables.Table):
    class Meta:
        model = Order
        fields = ['employee', 'material','quantity', 'order_date', 'notes']

class AccountTable(tables.Table):
    update = tables.TemplateColumn(
    '<a class="btn btn-success" href="/account?id={{ record.id }}">Update</a><a class="btn btn-danger mt-2" onclick="deleteModal(\'/account?\', {{ record.id }})"  data-bs-toggle="modal" data-bs-target="#deleteModal">Delete</a>',
        verbose_name='',
        orderable=False,
        attrs={
            "td": {"style": "max-width: min-content;"}
        }
    )

    class Meta:
        model = Account
        fields = ['id', 'user', 'phone_number', 'role']