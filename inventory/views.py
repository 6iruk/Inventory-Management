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
