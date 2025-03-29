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
            form.fields['stock_quantity'].required = False
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
                form.fields['stock_quantity'].disabled = True
        else:
            form = MaterialForm()

    else:
        form = None


    if 'query' in request.GET:
        materials = Material.objects.filter(Q(name__icontains = request.GET['query']) | Q(material_type__icontains = request.GET['query']) | Q(material_code__icontains = request.GET['query']) | Q(description__icontains = request.GET['query']))
        
        try:
            materials = materials.union(Material.objects.filter(Q(stock_quantity = float(request.GET['query'])) | Q(buying_price = float(request.GET['query'])) | Q(selling_price = float(request.GET['query']))))
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

            sale = form.save()
            sale.user = request.user
            sale.save()
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
        sales = Sale.objects.filter(Q(material__name__icontains = request.GET['query']) | Q(material__material_type__icontains = request.GET['query']) | Q(material__material_code__icontains = request.GET['query']) | Q(notes__icontains = request.GET['query']) | Q(sales_date__icontains = request.GET['query']))

        if request.GET['query'].isdigit():
            sales = sales.filter(Q(quantity = int(request.GET['query'])))
        
        try:
            sales = sales.union(Sale.objects.filter(Q(price = float(request.GET['query']))))
        except ValueError:
            pass

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
        if  request.POST.get('id'):
            id = int(request.POST['id'])
            employee = Employee.objects.get(id = id)
            form = EmployeeForm(request.POST, instance = employee)
        
        else:
            form = EmployeeForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("employee"))
    
    if request.GET.get('id'):
        id = int(request.GET['id'])
        employee = Employee.objects.get(id = id)

        if request.GET.get('del'):
            employee.delete()

            return HttpResponseRedirect(reverse("employee"))
        else:
            form = EmployeeForm(instance = employee)

    else:
        form = EmployeeForm()

    if 'query' in request.GET:
        employees = Employee.objects.filter(Q(name__icontains = request.GET['query']) | Q(phone_number__icontains = request.GET['query']) | Q(notes__icontains = request.GET['query']))
    
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

            order = form.save()
            order.user = request.user
            order.save()
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
        orders = Order.objects.filter(Q(material__name__icontains = request.GET['query']) | Q(material__material_type__icontains = request.GET['query']) | Q(material__material_code__icontains = request.GET['query']) | Q(employee__name__icontains = request.GET['query']) | Q(employee__phone_number__icontains = request.GET['query']) | Q(notes__icontains = request.GET['query']) | Q(order_date__icontains = request.GET['query']))

        if request.GET['query'].isdigit():
            orders = orders.filter(Q(quantity = int(request.GET['query'])))

        try:
            orders = orders.union(Order.objects.filter(Q(price = float(request.GET['query']))))
        except ValueError:
            pass

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
def account(request):
    
    role = ''
    if request.user.is_superuser:
        role = 'admin'
    
    else:

        return HttpResponseRedirect(reverse("home"))

    if request.method == "POST":
        if  request.POST.get('id'):
            id = int(request.POST['id'])
            account = Account.objects.get(id = id)
            form = AccountForm(request.POST, instance = account)
        
        else:
            form = AccountForm(request.POST)

        if form.is_valid() and request.POST.get('id'):
            data = form.cleaned_data
            account.user.username = data['username']
            account.user.set_password(data['password'])
            account.save()

            form.save()
            return HttpResponseRedirect(reverse("account"))
        
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['username'], password=data['password'])
            
            account = form.save(commit=False)
            account.user = user
            account.save()

            return HttpResponseRedirect(reverse("account"))
    
    if request.GET.get('id'):
        id = int(request.GET['id'])
        account = Account.objects.get(id = id)

        if request.GET.get('del'):
            account.delete()

            return HttpResponseRedirect(reverse("account"))
        else:
            form = AccountForm(instance = account)

    else:
        form = AccountForm()

    if 'query' in request.GET:
        accounts = Account.objects.filter(Q(name__icontains = request.GET['query']) | Q(phone_number__icontains = request.GET['query']) | Q(notes__icontains = request.GET['query']))
    
    else:
        accounts = Account.objects.all()
    
    if role == 'admin':
        table = AccountTable(accounts, order_by = request.GET.get('sort'))
    
    table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Account', "action_url":'account', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Account', "action_url":'account', "role":role})


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
    report_model = Sale
    date_field = "sales_date"
    group_by = "material"
    form_class = ReportForm
    columns = [
        "material_code",
        "buying_price",
        "selling_price",
        ComputationField.create(
            Sum, "quantity", name="quantity", verbose_name="Total Quantity"
        ),
        ComputationField.create(
            Sum, "price", name="etb_value", verbose_name="Total Value in ETB"
        ),
    ]

    chart_settings = [
        Chart(
            "Total quantity",
            Chart.COLUMN,
            data_source=["quantity"],
            title_source=["material_code"],
        ),
        Chart(
            "Total quantity [PIE]",
            Chart.PIE,
            data_source=["quantity"],
            title_source=["material_code"],
        ),
        Chart(
            "Total value in ETB",
            Chart.COLUMN,
            data_source=["etb_value"],
            title_source=["material_code"],
        ),
        Chart(
            "Total value in ETB [PIE]",
            Chart.PIE,
            data_source=["etb_value"],
            title_source=["material_code"],
        ),
    ]

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        if self.form.is_valid() and self.form.cleaned_data.get('report'):
            if self.form.cleaned_data['report'] == 'orders':
                self.__class__.queryset = Order.objects
                self.date_field = 'order_date'

            elif self.form.cleaned_data['report'] == 'purchases':
                self.__class__.queryset = Material.objects
                self.group_by = "material_code"
                self.date_field = 'purchase_date'
                self.columns = [
                    "material_code",
                    ComputationField.create(
                        Sum, "purchase_quantity", name="quantity", verbose_name="Total Purchase Quantity"
                    ),
                    ComputationField.create(
                        Sum, "total_cost", name="etb_cost", verbose_name="Total Cost in ETB"
                    ),
                    ComputationField.create(
                        Sum, "expected_sale", name="etb_value", verbose_name="Total Expected Profit in ETB"
                    ),
                ]

                self.chart_settings = [
                    Chart(
                        "Total quantity",
                        Chart.COLUMN,
                        data_source=["quantity"],
                        title_source=["material_code"],
                    ),
                    Chart(
                        "Total quantity [PIE]",
                        Chart.PIE,
                        data_source=["quantity"],
                        title_source=["material_code"],
                    ),
                    Chart(
                        "Total cost in ETB",
                        Chart.COLUMN,
                        data_source=["etb_cost"],
                        title_source=["material_code"],
                    ),
                    Chart(
                        "Total cost in ETB [PIE]",
                        Chart.PIE,
                        data_source=["etb_cost"],
                        title_source=["material_code"],
                    ),
                    Chart(
                        "Total value in ETB",
                        Chart.COLUMN,
                        data_source=["etb_value"],
                        title_source=["material_code"],
                    ),
                    Chart(
                        "Total value in ETB [PIE]",
                        Chart.PIE,
                        data_source=["etb_value"],
                        title_source=["material_code"],
                    ),
                ]

            elif self.form.cleaned_data['report'] == 'employees':
                self.__class__.queryset = Order.objects
                self.date_field = 'order_date'
                self.crosstab_field = "employee__code"
                self.crosstab_columns = [
                    ComputationField.create(
                        Sum, "quantity", name="order_quantity", verbose_name=" "
                    ),
                ]

                self.columns = [
                    "material_code",
                    "buying_price",
                    "__crosstab__",
                    ComputationField.create(
                        Sum, "quantity", name="quantity", verbose_name="Total Quantity"
                    ),
                    ComputationField.create(
                        Sum, "price", name="etb_value", verbose_name="Total Value in ETB"
                    ),
                ]

                self.chart_settings = [
                    Chart(
                        "Total quantity",
                        Chart.COLUMN,
                        data_source=["order_quantity"],
                        title_source=["material_code"],
                    ),
                ]
            
            else:
                self.__class__.queryset = Sale.objects

        return super().get(request, *args, **kwargs)