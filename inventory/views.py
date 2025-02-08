from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from inventory.forms import *
from django_tables2 import RequestConfig
from django.urls import reverse
from inventory.models import *
from inventory.tables import *

def material(request):
    
    if request.method == "POST":

        form = MaterialForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("home"))

    else:
        form = MaterialForm()

        if 'query' in request.GET:
            materials = Material.objects.filter(kifle = request.GET['query'])
        else:
            materials = Material.objects.all()
            
        table = MaterialTable(materials)
        table.paginate(page=request.GET.get("page", 1), per_page=4)
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"table":table, "form": form, "header":'Material', "action_url":'material'})
    else:
        return render(request, 'inventory/components/tables_full.html', {"table":table, "form": form, "header":'Material', "action_url":'material'})
