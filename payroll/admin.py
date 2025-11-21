from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
from .models import Institution, Position, Department, Employee


class InstitutionAdmin(ModelAdmin):
    list_display = ("name", "address", "phone")


class PositionAdmin(ModelAdmin):
    list_display = ("name",)


class DepartmentAdmin(ModelAdmin):
    list_display = ("name",)


class EmployeeAdmin(ModelAdmin):
    list_display = ("name", "email", "phone", "institution", "salary")


admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
