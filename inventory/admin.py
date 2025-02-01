from django.contrib import admin
from inventory.models import *

# Register your models here.
models = [Material]

for model in models:
	admin.site.register(model)