from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import User

# Create your models here

USER_ROLES = (
    ('ADMIN', 'Admin'),
    ('MANAGER', 'Manager'),
    ('CASHIER', 'Cashier'),
)

EMPLOYEE_TYPES = [
    ('FULL', 'Full Time'),
    ('PART', 'Part Time'),
]

DEPARTMENTS = [
    ('CHAIR', 'Chair'),
    ('TABLE', 'Table'),
]

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Material(models.Model):
    name = models.CharField(max_length=100)
    material_type = models.CharField(max_length=100)
    material_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    buying_price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    selling_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.material_code + '-' + self.material_type + '-' + self.name

class Sale(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    sales_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.material.material_code +  ' - ' + str(self.quantity)

    def save(self, **kwargs):
        self.material.stock_quantity -= self.quantity
        self.price = self.quantity * self.material.selling_price
        self.material.save()

        super().save(**kwargs)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.phone_number
    
class Order(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    quantity = models.PositiveIntegerField()
    order_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.material + str(self.quantity)

    def save(self, **kwargs):
        self.material.stock_quantity -= self.quantity
        self.price = self.quantity * self.material.selling_price
        self.material.save()
        
        super().save(**kwargs)

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, unique=True)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    
    def __str__(self):
        return self.phone_number