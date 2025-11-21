# Guía de Instalación y Pruebas - Sistema de Nómina

Esta guía detalla los pasos para configurar, ejecutar y probar el proyecto en cualquier entorno local.

## 📋 Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

## 🚀 Instalación y Configuración

1.  **Clonar el repositorio** (si no lo has hecho aún):
    ```bash
    git clone <url-del-repositorio>
    cd <nombre-carpeta>
    ```

2.  **Crear y activar un entorno virtual**:
    *   Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos**:
    Realizar las migraciones para crear las tablas:
    ```bash
    python manage.py migrate
    ```

5.  **Cargar datos de prueba**:
    El proyecto incluye un fixture con datos iniciales (instituciones, empleados, etc.):
    ```bash
    python manage.py loaddata payroll/fixtures/initial_data.json
    ```

## ▶️ Ejecución

Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```
El servidor estará disponible en `http://127.0.0.1:8000/`.

## 🧪 Guía de Pruebas (Endpoints)

Aquí tienes las URLs para probar las funcionalidades principales implementadas.

### 1. Filtros Avanzados de Empleados
*   **Filtrar por Rango de Salario**:
    `GET /api/employees/?min_salary=30000&max_salary=50000`
*   **Filtrar por Instituciones Múltiples**:
    `GET /api/employees/?institutions=1,2`
*   **Filtrar por Fecha de Contratación**:
    `GET /api/employees/?hire_date_from=2023-01-01`
*   **Combinado**:
    `GET /api/employees/?min_salary=30000&institutions=1&hire_date_from=2020-01-01`

### 2. Salario por Hora
Calcula el salario por hora basado en el salario mensual.
*   **Cálculo Estándar (160 horas)**:
    `GET /api/employees/1/salary_per_hour/`
*   **Cálculo Personalizado (ej. 200 horas)**:
    `GET /api/employees/1/salary_per_hour/?hours=200`

### 3. Reporte de Nómina Mensual (CSV)
Descarga un archivo CSV con el reporte de nómina.
*   **Parámetros requeridos**: `month` (YYYY-MM) y `institution` (ID).
    `GET /api/payroll-report/?month=2024-03&institution=1`
*   **Opcional**: Filtrar por departamento.
    `GET /api/payroll-report/?month=2024-03&institution=1&department=1`

## 🛠️ Ejecutar Tests Automáticos

Para correr los tests unitarios del proyecto:
```bash
python manage.py test
```
