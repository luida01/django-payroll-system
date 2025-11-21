from rest_framework import serializers
from .models import Employee, Position, Department, TimeEntry, Institution


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    institution = serializers.PrimaryKeyRelatedField(queryset=Institution.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), allow_null=True, required=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Employee
        fields = '__all__'

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("El salario debe ser mayor a cero.")
        return value

    def validate_hourly_rate(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("La tarifa por hora debe ser mayor a cero.")
        return value

    def validate_email(self, value):
        if not value.endswith("@empresa.com"):
            raise serializers.ValidationError("El correo debe pertenecer al dominio @empresa.com.")
        return value



class TimeEntrySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    payment = serializers.SerializerMethodField()

    class Meta:
        model = TimeEntry
        fields = '__all__'

    def get_payment(self, obj):
        return obj.calculate_payment()

    def validate_hours_worked(self, value):
        if value <= 0:
            raise serializers.ValidationError("Las horas trabajadas deben ser mayores a cero.")
        if value > 24:
            raise serializers.ValidationError("No puedes registrar mas de 24 horas en un dia.")
        return value

