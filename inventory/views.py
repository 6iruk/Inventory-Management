from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from inventory.forms import *
from django_tables2 import RequestConfig
from django.urls import reverse
from inventory.models import *

def material(request):
    
    if request.method == "POST":

        form = MaterialForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("home"))

    else:
        form = MaterialForm()
    
    if request.htmx:
        return render(request, 'inventory/components/tables.html', {"form": form, "header":'Material', "action_url":'material'})
    else:
        return render(request, 'inventory/components/tables_full.html', {"form": form, "header":'Material', "action_url":'material'})
