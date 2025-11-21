# 🏢 Django Payroll System

REST API built with Django for employee payroll management.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![Django](https://img.shields.io/badge/django-4.0+-green.svg)]()
[![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)]()

## 📋 Features

- ✅ Complete CRUD operations for Institutions, Departments, Positions, and Employees
- 🔍 Advanced filtering (salary range, multiple values, date ranges)
- 💰 Hourly salary calculations
- 📊 Monthly payroll CSV reports
- ✔️ Data validation and relationship handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/luida01/django-payroll-system.git
cd django-payroll-system
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Load initial data
```bash
python manage.py loaddata fixtures/initial_data.json
```

5. Run server
```bash
python manage.py runserver
```

## 📚 API Endpoints

### CRUD Operations
- `GET/POST /api/institutions/`
- `GET/PUT/DELETE /api/institutions/{id}/`
- Similar endpoints for employees, departments, positions

### Special Endpoints
- `GET /api/employees/{id}/salary_per_hour/?hours=160`
- `GET /api/payroll/monthly-report/?month=2024-03&institution=1`

## 🔍 Filtering Examples
```bash
# Salary range
GET /api/employees/?min_salary=30000&max_salary=50000

# Multiple institutions
GET /api/employees/?institutions=1,2,3&departments=5,6

# Date range
GET /api/employees/?hire_date_from=2023-01-01&hire_date_to=2024-12-31

# Combined filters
GET /api/employees/?min_salary=35000&institutions=1,2&hire_date_from=2023-01-01
```

## 📊 CSV Report Format

The monthly payroll report includes:
- Employee details (name, email, institution, department, position)
- Salary calculations (monthly, hourly)
- Totals by institution and department

## ✅ Validations

- Phone numbers: `+1XXXXXXXXXX` format
- Email: Valid and unique
- Salary: Positive values only
- Required relationships validation

## 🛠️ Tech Stack

- Django 4.x
- Django REST Framework
- Python 3.8+

## 📝 License

MIT License

## 👤 Author

**Luis Daniel Santana Mercado**
- GitHub: [@luida01](https://github.com/luida01)
- Email: luisdanielsantanamercado@gmail.com
