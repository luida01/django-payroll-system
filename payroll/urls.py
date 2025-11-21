from django.urls import path, include
from rest_framework import routers
from .views import (
    InstitutionViewSet,
    PositionViewSet,
    DepartmentViewSet,
    EmployeeViewSet,
    TimeEntryViewSet,
    payroll_csv_report,
)

router = routers.DefaultRouter()
router.register("institutions", InstitutionViewSet)
router.register("positions", PositionViewSet)
router.register("departments", DepartmentViewSet)
router.register("employees", EmployeeViewSet)
router.register("timeentries", TimeEntryViewSet)

urlpatterns = [
    path("", include(router.urls)),           
    path("payroll-report/", payroll_csv_report, name="payroll-report"), 
]
