from django.contrib import admin
from django.urls import path
from dashboard import views

urlpatterns = [
    # 🔐 LOGIN & LOGOUT
    path("", views.dashboard_login, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # 📊 Dashboard principal
    path("dashboard/", views.admin_dashboard, name="dashboard_home"),

    # 📋 Listas
    path("dashboard/usuarios/", views.dashboard_usuarios, name="dashboard_usuarios"),
    path("dashboard/tareas/", views.dashboard_tareas, name="dashboard_tareas"),
    path("dashboard/eventos/", views.dashboard_eventos, name="dashboard_eventos"),

    # ➕ Formularios (crear nuevo)
    path("dashboard/tareas/nuevo/", views.tarea_nueva, name="tarea_nueva"),
    path("dashboard/eventos/nuevo/", views.evento_nuevo, name="evento_nuevo"),
    path("dashboard/usuarios/nuevo/", views.usuario_nuevo, name="usuario_nuevo"),
    path("dashboard/habitos/nuevo/", views.habito_nuevo, name="habito_nuevo"),

    # ⚙️ Admin Django original
    path("admin/", admin.site.urls),
]