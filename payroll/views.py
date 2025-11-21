from django.http import HttpResponse
import csv
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Institution, Position, Department, Employee, TimeEntry
from .serializers import (
    InstitutionSerializer,
    PositionSerializer,
    DepartmentSerializer,
    EmployeeSerializer,
    TimeEntrySerializer,
)


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


from .filters import EmployeeFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeFilter

    @action(detail=True, methods=['get'])
    def salary_per_hour(self, request, pk=None):
        employee = self.get_object()
        hours_param = request.query_params.get('hours', '160')
        
        try:
            hours = Decimal(hours_param)
            if hours <= 0:
                raise ValueError
        except:
            return Response({"error": "Las horas deben ser un número positivo."}, status=400)
            
        salary_per_hour = employee.salary / hours
        
        return Response({
            "employee": employee.name,
            "monthly_salary": employee.salary,
            "hours": hours,
            "salary_per_hour": round(salary_per_hour, 2)
        })


class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'date']


from collections import defaultdict

def payroll_csv_report(request):
    # 1. Validate Parameters
    month = request.GET.get('month')
    institution_id = request.GET.get('institution')
    department_id = request.GET.get('department')

    if not month or not institution_id:
        return HttpResponse("Missing required parameters: month and institution", status=400)

    # 2. Filter Employees
    employees = Employee.objects.filter(
        institution_id=institution_id,
        is_active=True
    )
    
    if department_id:
        employees = employees.filter(department_id=department_id)

    # 3. Prepare Response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="payroll_report_{month}.csv"'
    
    writer = csv.writer(response)
    
    # 4. Write Headers
    writer.writerow([
        'Employee Name', 'Email', 'Institution', 'Department', 'Position', 
        'Monthly Salary', 'Hours Worked', 'Hourly Salary'
    ])

    # 5. Initialize Totals
    total_employees = 0
    total_payroll = Decimal('0.00')
    total_hours = 0
    
    # Grouping structures
    inst_stats = defaultdict(lambda: {'count': 0, 'payroll': Decimal('0.00'), 'hours': 0})
    dept_stats = defaultdict(lambda: {'count': 0, 'payroll': Decimal('0.00'), 'hours': 0})

    # 6. Process Employees
    hours_default = 160  # Fixed for this requirement
    
    for emp in employees:
        # Calculations
        monthly_salary = emp.salary
        hourly_salary = monthly_salary / hours_default
        
        # Write Row
        writer.writerow([
            emp.name,
            emp.email,
            emp.institution.name,
            emp.department.name if emp.department else "N/A",
            emp.position.name if emp.position else "N/A",
            monthly_salary,
            hours_default,
            round(hourly_salary, 2)
        ])
        
        # Update Totals
        total_employees += 1
        total_payroll += monthly_salary
        total_hours += hours_default
        
        # Update Groups
        # Institution
        inst_name = emp.institution.name
        inst_stats[inst_name]['count'] += 1
        inst_stats[inst_name]['payroll'] += monthly_salary
        inst_stats[inst_name]['hours'] += hours_default
        
        # Department
        dept_name = emp.department.name if emp.department else "No Department"
        dept_stats[dept_name]['count'] += 1
        dept_stats[dept_name]['payroll'] += monthly_salary
        dept_stats[dept_name]['hours'] += hours_default

    # 7. Write Totals Sections
    writer.writerow([])
    writer.writerow(['TOTALS'])
    writer.writerow(['Total Employees', total_employees])
    writer.writerow(['Total Payroll', total_payroll])
    writer.writerow(['Total Hours', total_hours])
    
    writer.writerow([])
    writer.writerow(['BY INSTITUTION'])
    for name, stats in inst_stats.items():
        writer.writerow([name, stats['count'], stats['payroll'], stats['hours']])
        
    writer.writerow([])
    writer.writerow(['BY DEPARTMENT'])
    for name, stats in dept_stats.items():
        writer.writerow([name, stats['count'], stats['payroll'], stats['hours']])

    return response
