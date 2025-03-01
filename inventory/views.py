from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
from django_tables2 import RequestConfig
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
    
    role = ''
    if request.user.is_superuser:
        role = 'admin'
    
    else:

        user = Account.objects.get(user=request.user)
        role = user.role.lower()

    if request.method == "POST":

        form = MaterialForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("home"))

    else:
        form = MaterialForm()

    if 'query' in request.GET:
        materials = Material.objects.filter(Q(name__icontains = request.GET['query']) | Q(material_type__icontains = request.GET['query']) | Q(material_code__icontains = request.GET['query']))

        if request.GET['query'].isdigit():
            materials = materials.filter(Q(stock_quantity = int(request.GET['query'])))
        
        try:
            materials = materials.filter(Q(buying_price = float(request.GET['query'])) | Q(unit_price = float(request.GET['query'])))
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

        form = SaleForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("sale"))

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
        table = SaleTable(sales, order_by = request.GET.get('sort'))
    
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

        form = OrderForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("order"))

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
        table = OrderTable(orders, order_by = request.GET.get('sort'))
    
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
            table = OrderTable(orders)
        
        table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Order', "action_url":'material', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Order', "action_url":'material', "role":role})