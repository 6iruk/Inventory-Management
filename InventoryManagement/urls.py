"""
URL configuration for InventoryManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from inventory import views

urlpatterns = [
    path('login',
            auth_views.LoginView.as_view(template_name="inventory/login.html"), name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.material, name='home'),
    path('material', views.material, name='material'),
    path('sale', views.sale, name='sale'),
    path('employee', views.employee, name='employee'),
    path('order', views.order, name='order'),
    path('account', views.account, name='account'),
    path('report', views.report, name='report'),
    path("sale-report", views.SaleReport.as_view(), name='sale-report'),
    path('admin/', admin.site.urls),
]
