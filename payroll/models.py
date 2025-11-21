from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator
from decimal import Decimal

# Validator for phone numbers
phone_validator = RegexValidator(
    regex=r'^\+1\d{10}$',
    message="El teléfono debe tener el formato +1XXXXXXXXX (10 dígitos después del +1)."
)

class Institution(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()  # Made required (removed blank=True)
    phone = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=True,
        blank=True
    )
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.salary <= 0:
            raise ValidationError("El salario debe ser mayor a cero.")
        if self.hourly_rate is not None and self.hourly_rate <= 0:
            raise ValidationError("La tarifa por hora debe ser mayor a cero.")

class TimeEntry(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    hours_worked = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date']

    def calculate_payment(self):
        if self.employee.hourly_rate:
            return self.hours_worked * self.employee.hourly_rate
        return Decimal('0.00')
    
    def __str__(self):
        return f"{self.employee} - {self.date}"