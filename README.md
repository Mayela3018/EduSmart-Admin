# 🎓 EDUSMART - DJANGO ADMIN PANEL
## Guía de Instalación Completa

---

## 📋 REQUISITOS PREVIOS

- Python 3.10 o superior
- PostgreSQL instalado y corriendo
- pip (gestor de paquetes de Python)
- Base de datos de EduSmart (Spring Boot) ya creada

---

## 🚀 PASO 1: CREAR EL PROYECTO

### 1.1 Crear carpeta del proyecto

bash
mkdir edusmart-admin
cd edusmart-admin


### 1.2 Crear entorno virtual

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate


### 1.3 Instalar dependencias

bash
pip install -r requirements.txt


---

## 🗂 PASO 2: CREAR ESTRUCTURA DEL PROYECTO

### 2.1 Crear proyecto Django

bash
django-admin startproject edusmart_admin .


### 2.2 Crear app dashboard

bash
python manage.py startapp dashboard


### 2.3 Estructura final:


edusmart-admin/
├── venv/
├── edusmart_admin/
│   ├── __init__.py
│   ├── settings.py      ← REEMPLAZAR con el archivo proporcionado
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── dashboard/
│   ├── __init__.py
│   ├── models.py        ← REEMPLAZAR con el archivo proporcionado
│   ├── admin.py         ← REEMPLAZAR con el archivo proporcionado
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── static/
├── templates/
├── manage.py
├── requirements.txt
├── .env                 ← CREAR desde .env.example
└── README.md


---

## ⚙ PASO 3: CONFIGURAR LA BASE DE DATOS

### 3.1 Crear archivo .env

Copia .env.example a .env y completa con tus credenciales:

env
# Database Configuration
DB_NAME=edusmart_db          ← Nombre de tu BD
DB_USER=postgres             ← Tu usuario PostgreSQL
DB_PASSWORD=tu_contraseña    ← Tu contraseña
DB_HOST=localhost
DB_PORT=5432

# Django Settings
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1


### 3.2 Verificar conexión a la BD

bash
python manage.py dbshell


Si se conecta correctamente, verás el prompt de PostgreSQL:

psql (15.x)
Type "help" for help.

edusmart_db=#


Sal con: \q

---

## 📊 PASO 4: GENERAR MODELOS DESDE LA BD

### 4.1 Inspeccionar las tablas existentes

bash
python manage.py inspectdb


Este comando muestra los modelos generados automáticamente.

### 4.2 Guardar los modelos

bash
python manage.py inspectdb > dashboard/models_generated.py


### 4.3 Revisar y ajustar

1. Abre dashboard/models_generated.py
2. Compara con dashboard/models.py (el archivo proporcionado)
3. Ajusta los nombres de las tablas si es necesario
4. Asegúrate que managed = False esté en todas las clases Meta

### 4.4 IMPORTANTE: NO ejecutar migraciones

❌ *NO hagas esto:*
bash
python manage.py makemigrations
python manage.py migrate


✅ *Solo ejecuta:*
bash
python manage.py migrate --fake


Esto marca las migraciones de Django como aplicadas SIN tocar la BD.

---

## 👤 PASO 5: CREAR SUPERUSUARIO

### 5.1 Crear superusuario de Django

bash
python manage.py createsuperuser


Ingresa:
- Username: admin
- Email: admin@edusmart.com
- Password: ******* (o la que prefieras)

*IMPORTANTE:* Este usuario es SOLO para Django Admin, NO está en la tabla admin_users.

---

## 🎨 PASO 6: CONFIGURAR ARCHIVOS

### 6.1 Reemplazar archivos

Copia los archivos proporcionados:

1. *edusmart_admin/settings.py* ← settings.py proporcionado
2. *dashboard/models.py* ← models.py proporcionado
3. *dashboard/admin.py* ← admin.py proporcionado

### 6.2 Agregar dashboard a INSTALLED_APPS

En settings.py, verifica que 'dashboard' esté en INSTALLED_APPS:

python
INSTALLED_APPS = [
    # ...
    'dashboard',  ← Debe estar aquí
]


### 6.3 Configurar URLs

En edusmart_admin/urls.py:

python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


---

## ▶ PASO 7: EJECUTAR EL SERVIDOR

### 7.1 Recolectar archivos estáticos

bash
python manage.py collectstatic --noinput


### 7.2 Iniciar servidor

bash
python manage.py runserver 8000


### 7.3 Acceder al admin

Abre tu navegador en:

http://localhost:8000/admin/


Inicia sesión con el superusuario que creaste.

---

## ✅ PASO 8: VERIFICACIÓN

### 8.1 Verifica que veas estos módulos en el admin:

- ✅ *Usuarios* (AdminUser)
- ✅ *Tareas* (Task)
- ✅ *Eventos* (Event)
- ✅ *Hábitos* (Habit)

### 8.2 Verifica que los datos existan

Haz clic en cada módulo y deberías ver los datos de Spring Boot.

### 8.3 Prueba funcionalidades

- Buscar usuarios
- Filtrar tareas por prioridad
- Ver eventos del día
- Exportar datos a CSV

---

## 🎨 PERSONALIZACIÓN ADICIONAL

### Dashboard personalizado (opcional)

Si quieres un dashboard con gráficos, puedes crear:

1. *dashboard/views.py* con vistas personalizadas
2. *templates/admin/* con templates custom
3. *static/css/* con estilos adicionales

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "relation does not exist"

- *Causa:* Los nombres de las tablas no coinciden
- *Solución:* Ejecuta python manage.py inspectdb y verifica los nombres exactos

### Error: "no password supplied"

- *Causa:* Falta la contraseña en .env
- *Solución:* Completa DB_PASSWORD en .env

### Error: "FATAL: role does not exist"

- *Causa:* El usuario de PostgreSQL no existe
- *Solución:* Verifica DB_USER en .env

### Los datos no aparecen

- *Causa:* managed = False no está configurado
- *Solución:* Agrega managed = False en Meta de cada modelo

---

## 📚 COMANDOS ÚTILES

bash
# Ver información de la BD
python manage.py dbshell

# Ver modelos registrados
python manage.py shell
>>> from dashboard.models import Task
>>> Task.objects.count()

# Limpiar caché
python manage.py clear_cache

# Ver logs en tiempo real
python manage.py runserver --verbosity 3


---

## 🎯 PRÓXIMOS PASOS

1. ✅ Personalizar colores del admin
2. ✅ Agregar dashboard con estadísticas
3. ✅ Crear reportes personalizados
4. ✅ Configurar permisos por rol
5. ✅ Agregar notificaciones

---

## 📞 SOPORTE

Si tienes problemas:
1. Verifica que PostgreSQL esté corriendo
2. Revisa los logs: python manage.py runserver --verbosity 3
3. Verifica las credenciales en .env
4. Asegúrate que Spring Boot no esté usando la BD al mismo tiempo

---

¡Listo! Ahora tienes el Django Admin Panel conectado a tu base de datos. 🎉