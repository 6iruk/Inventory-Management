from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
from django_tables2 import RequestConfig
from django.db.models import Sum
from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField
from inventory.forms import *
from django.urls import reverse
from inventory.models import *
from inventory.tables import *

@login_required    
def logout(request):

    auth_logout(request)

    return HttpResponseRedirect(reverse("login"))

@login_required
def material(request):
    
    if request.user.is_superuser:
        role = 'admin'
    
    else:

        user = Account.objects.get(user=request.user)
        role = user.role.lower()


    if request.method == "POST" and role == 'admin':
        if request.POST.get('id'):
            id = int(request.POST['id'])
            material = Material.objects.get(id = id)
            form = MaterialForm(request.POST, instance = material)
        
        else:
            form = MaterialForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("material"))

    elif role == 'admin':
        if request.GET.get('id'):
            id = int(request.GET['id'])
            material = Material.objects.get(id = id)

            if request.GET.get('del'):
                material.delete()

                return HttpResponseRedirect(reverse("material"))
            else:
                form = MaterialForm(instance = material)

        else:
            form = MaterialForm()

    else:
        form = None


    if 'query' in request.GET:
        materials = Material.objects.filter(Q(name__icontains = request.GET['query']) | Q(material_type__icontains = request.GET['query']) | Q(material_code__icontains = request.GET['query']) | Q(description__icontains = request.GET['query']))
        
        try:
            materials = materials.union(Material.objects.filter(Q(stock_quantity = float(request.GET['query'])) | Q(buying_price = float(request.GET['query'])) | Q(unit_price = float(request.GET['query']))))
        except ValueError:
            pass
    else:
        materials = Material.objects.all()
    
    if role == 'admin':
        table = MaterialTable(materials, order_by = request.GET.get('sort'))
    elif role == 'manager':
        table = ManagerMaterialTable(materials, order_by = request.GET.get('sort'))
    elif role == 'cashier':
        table = CashierMaterialTable(materials, order_by = request.GET.get('sort'))
    
    table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Material', "action_url":'material', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Material', "action_url":'material', "role":role})

@login_required
def sale(request):
    
    role = ''
    if request.user.is_superuser:
        role = 'admin'
    
    else:

        user = Account.objects.get(user=request.user)
        role = user.role.lower()

    if request.method == "POST":
        if  role == 'admin' and request.POST.get('id'):
            id = int(request.POST['id'])
            sale = Sale.objects.get(id = id)
            form = SaleForm(request.POST, instance = sale)
        
        else:
            form = SaleForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("sale"))

    elif role == 'admin':
        if request.GET.get('id'):
            id = int(request.GET['id'])
            sale = Sale.objects.get(id = id)

            if request.GET.get('del'):
                sale.delete()

                return HttpResponseRedirect(reverse("sale"))
            else:
                form = SaleForm(instance = sale)

        else:
            form = SaleForm()

    else:
        form = SaleForm()

    if 'query' in request.GET:
        sales = Sale.objects.filter(Q(material__name__icontains = request.GET['query']) | Q(material__material_type__icontains = request.GET['query']) | Q(material__material_code__icontains = request.GET['query']))

        if request.GET['query'].isdigit():
            sales = sales.filter(Q(quantity = int(request.GET['query'])))
    
    else:
        sales = Sale.objects.all()
    
    if role == 'admin':
        table = SaleTable(sales, order_by = request.GET.get('sort'))
    elif role == 'cashier':
        table = CashierSaleTable(sales, order_by = request.GET.get('sort'))
    
    table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Sale', "action_url":'sale', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Sale', "action_url":'sale', "role":role})

@login_required
def employee(request):
    
    role = ''
    if request.user.is_superuser:
        role = 'admin'
    
    else:

        return HttpResponseRedirect(reverse("home"))

    if request.method == "POST":

        form = EmployeeForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("employee"))

    else:
        form = EmployeeForm()

    if 'query' in request.GET:
        employees = Employee.objects.filter(Q(name__icontains = request.GET['query']) | Q(phone_number__icontains = request.GET['query']))
    
    else:
        employees = Employee.objects.all()
    
    if role == 'admin':
        table = EmployeeTable(employees, order_by = request.GET.get('sort'))
    
    table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Employee', "action_url":'employee', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Employee', "action_url":'employee', "role":role})
      
@login_required
def order(request):
    
    role = ''
    if request.user.is_superuser:
        role = 'admin'
    
    else:

        user = Account.objects.get(user=request.user)
        role = user.role.lower()

    if request.method == "POST":
        if  role == 'admin' and request.POST.get('id'):
            id = int(request.POST['id'])
            order = Order.objects.get(id = id)
            form = OrderForm(request.POST, instance = order)
        
        else:
            form = OrderForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("order"))

    elif role == 'admin':
        if request.GET.get('id'):
            id = int(request.GET['id'])
            order = Order.objects.get(id = id)

            if request.GET.get('del'):
                order.delete()

                return HttpResponseRedirect(reverse("order"))
            else:
                form = OrderForm(instance = order)

        else:
            form = OrderForm()

    else:
        form = OrderForm()

    if 'query' in request.GET:
        orders = Order.objects.filter(Q(material__name__icontains = request.GET['query']) | Q(material__material_type__icontains = request.GET['query']) | Q(material__material_code__icontains = request.GET['query']) | Q(employee__name__icontains = request.GET['query']) | Q(employee__phone_number__icontains = request.GET['query']))

        if request.GET['query'].isdigit():
            orders = orders.filter(Q(quantity = int(request.GET['query'])))
    
    else:
        orders = Order.objects.all()
    
    if role == 'admin':
        table = OrderTable(orders, order_by = request.GET.get('sort'))
    elif role == 'manager':
        table = ManagerOrderTable(orders, order_by = request.GET.get('sort'))
    
    table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Order', "action_url":'order', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Order', "action_url":'order', "role":role})

@login_required
def user(request):
    
    role = ''
    if request.user.is_superuser:
        role = 'admin'
    
    else:

        user = Account.objects.get(user=request.user)
        role = user.role.lower()

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("order"))

    else:
        form = OrderForm()

        if 'query' in request.GET:
            orders = Order.objects.filter(material_code = request.GET['query'])
        else:
            orders = Order.objects.all()
        
        if role == 'admin':
            table = OrderTable(orders)
        elif role == 'manager':
            table = ManagerOrderTable(orders)
        
        table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Order', "action_url":'material', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Order', "action_url":'material', "role":role})

@login_required
def report(request):
    
    role = ''
    if request.user.is_superuser:
        role = 'admin'
    
    else:
        return HttpResponseRedirect(reverse("home"))
    
    report = SaleReport.as_view()(request)
    if request.htmx or request.GET.get('_export') or request.headers.get('X-Requested-With') and request.headers['X-Requested-With'] == 'XMLHttpRequest':
        return report
    else:
        return render(request, 'inventory/components/report_full.html', {'report': report.render().content.decode('utf-8'), 'role': role})

class SaleReport(ReportView):
    report_title = "Dashboard"
    report_model = Material
    date_field = "sale__sales_date"
    group_by = "material_code"
    form_class = ReportForm
    columns = [
        "material_code",
        ComputationField.create(
            Sum, "sale__quantity", verbose_name="Total Sales Quantity"
        ),
        ComputationField.create(
            Sum, "sale__price", name="sales__value", verbose_name="Total Sales Value in ETB"
        ),
    ]

    chart_settings = [
        Chart(
            "Total sales in ETB",
            Chart.COLUMN,
            data_source=["sales__value"],
            title_source=["material_code"],
        ),
        Chart(
            "Total sales in ETB [PIE]",
            Chart.PIE,
            data_source=["sales__value"],
            title_source=["material_code"],
        ),
    ]

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        if self.form.is_valid() and self.form.cleaned_data.get('report'):
            if self.form.cleaned_data['report'] == 'orders':
                self.date_field = 'order__order_date'
                self.columns = [
                    "material_code",
                    ComputationField.create(
                        Sum, "order__quantity", name="orders__value", verbose_name="Total Order Quantity"
                    ),
                    ComputationField.create(
                        Sum, "order__price", verbose_name="Total Orders Value in ETB"
                    ),
                ]

                self.chart_settings = [
                    Chart(
                        "Total Work Orders in ETB",
                        Chart.COLUMN,
                        data_source=["orders__value"],
                        title_source=["material_code"],
                    ),
                    Chart(
                        "Total Work Orders in ETB [PIE]",
                        Chart.PIE,
                        data_source=["orders__value"],
                        title_source=["material_code"],
                    ),
                ]
        
        return super().get(request, *args, **kwargs)