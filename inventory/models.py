from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

# Create your models here

USER_ROLES = (
    ('ADMIN', 'Admin'),
    ('MANAGER', 'Manager'),
)

EMPLOYEE_TYPES = [
    ('FULL', 'Full Time'),
    ('PART', 'Part Time'),
]

DEPARTMENTS = [
    ('CHAIR', 'Chair'),
    ('TABLE', 'Table'),
]

REQUEST_STATUS = [
    ('PENDING', 'Pending'),
    ('ACCEPTED', 'Accepted'),
    ('PROCESSING', 'Processing'),
    ('IN_TRANSIT', 'In Transit'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled')
]

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class User(AbstractUser):
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, unique=True)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

class Material(models.Model):
    name = models.CharField(max_length=100)
    material_type = models.CharField(max_length=100)
    material_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    unit_name = models.CharField(max_length=50)
    unit_symbol = models.CharField(max_length=10)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    photo = models.EmailField(unique=True, null=True, blank=True)
    department_name =  models.CharField(max_length=20, choices=DEPARTMENTS)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPES)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

class Usage(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    request_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

class Procurement(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    request_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='PENDING')
    notes = models.TextField(blank=True, null=True)