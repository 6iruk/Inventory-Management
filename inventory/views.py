from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
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
            materials = Material.objects.filter(material_code = request.GET['query'])
        else:
            materials = Material.objects.all()
        
        if role == 'admin':
            table = MaterialTable(materials)
        elif role == 'manager':
            table = ManagerMaterialTable(materials)
        elif role == 'cashier':
            table = CashierMaterialTable(materials)
        
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
            sales = Sale.objects.filter(material_code = request.GET['query'])
        else:
            sales = Sale.objects.all()
        
        if role == 'admin':
            table = SaleTable(sales)
        elif role == 'cashier':
            table = SaleTable(sales)
        
        table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Sale', "action_url":'material', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Sale', "action_url":'material', "role":role})

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
            employees = Employee.objects.filter(material_code = request.GET['query'])
        else:
            employees = Employee.objects.all()
        
        if role == 'admin':
            table = EmployeeTable(employees)
        
        table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Employee', "action_url":'material', "role":role})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Employee', "action_url":'material', "role":role})
      
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