# dashboard/admin.py
# Configuración del Django Admin Panel - VERSIÓN CORRECTA

from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import Users, Tasks, Events, Habits


# ============================================
# USUARIOS
# ============================================

@admin.register(Users)
class UsersAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name_display', 'email', 'tipo_badge', 'tasks_count', 'created_display']
    list_filter = ['tipo', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['id', 'created_at', 'password']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('name', 'email', 'tipo')
        }),
        ('TECSUP', {
            'fields': ('tecsup_token',),
            'classes': ('collapse',)
        }),
        ('Preferencias', {
            'fields': ('preferences',),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('id', 'created_at', 'password'),
            'classes': ('collapse',)
        }),
    )
    
    def name_display(self, obj):
        return format_html(
            '<strong style="color: #667eea;">{}</strong>',
            obj.name or 'Sin nombre'
        )
    name_display.short_description = 'Nombre'
    
    def tipo_badge(self, obj):
        colors = {
            'ADMIN': '#ef4444',
            'ESTUDIANTE': '#3b82f6',
            'GENERAL': '#6b7280',
        }
        color = colors.get(obj.tipo, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: 700;">{}</span>',
            color, obj.tipo or 'N/A'
        )
    tipo_badge.short_description = 'Tipo'
    
    def tasks_count(self, obj):
        count = Tasks.objects.filter(user=obj).count()
        return format_html(
            '<span style="color: #667eea; font-weight: 700;">📋 {}</span>',
            count
        )
    tasks_count.short_description = 'Tareas'
    
    def created_display(self, obj):
        if obj.created_at:
            return obj.created_at.strftime('%d/%m/%Y')
        return 'N/A'
    created_display.short_description = 'Creado'


# ============================================
# TAREAS
# ============================================

@admin.register(Tasks)
class TasksAdmin(ImportExportModelAdmin):
    list_display = ['id', 'titulo_display', 'priority_badge', 'source_badge', 
                    'status_badge', 'fecha_limite', 'user_link']
    list_filter = ['prioridad', 'completed', 'source', 'created_at']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['id', 'created_at', 'updated_at', 'tecsup_external_id']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información de la Tarea', {
            'fields': ('titulo', 'descripcion')
        }),
        ('Detalles', {
            'fields': ('prioridad', 'fecha_limite', 'completed')
        }),
        ('Origen', {
            'fields': ('source', 'sincronizado_tecsup', 'tecsup_external_id', 'user')
        }),
        ('Sistema', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marcar_completadas', 'marcar_pendientes', 'cambiar_prioridad_alta']
    
    def titulo_display(self, obj):
        icon = '✅' if obj.completed else '📋'
        return format_html(
            '{} <strong>{}</strong>',
            icon, obj.titulo
        )
    titulo_display.short_description = 'Título'
    
    def priority_badge(self, obj):
        colors = {
            'ALTA': '#ef4444',
            'MEDIA': '#f59e0b',
            'BAJA': '#10b981',
        }
        color = colors.get(obj.prioridad, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: 700;">{}</span>',
            color, obj.prioridad
        )
    priority_badge.short_description = 'Prioridad'
    
    def source_badge(self, obj):
        if obj.source == 'TECSUP':
            return format_html(
                '<span style="background: #3b82f6; color: white; padding: 4px 12px; '
                'border-radius: 12px; font-size: 11px; font-weight: 700;">🏫 TECSUP</span>'
            )
        return format_html(
            '<span style="color: #6b7280; font-size: 11px;">Manual</span>'
        )
    source_badge.short_description = 'Origen'
    
    def status_badge(self, obj):
        if obj.completed:
            return format_html(
                '<span style="color: #10b981; font-weight: 700;">✅ Completada</span>'
            )
        return format_html(
            '<span style="color: #f59e0b; font-weight: 700;">⏳ Pendiente</span>'
        )
    status_badge.short_description = 'Estado'
    
    def user_link(self, obj):
        if obj.user:
            return format_html(
                '<a href="/admin/dashboard/users/{}/change/" style="color: #667eea;">👤 {}</a>',
                obj.user.id, obj.user.name or obj.user.email
            )
        return format_html('<span style="color: #ef4444;">Sin usuario</span>')
    user_link.short_description = 'Usuario'
    
    # Acciones masivas
    def marcar_completadas(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f'{updated} tareas marcadas como completadas.')
    marcar_completadas.short_description = '✅ Marcar como completadas'
    
    def marcar_pendientes(self, request, queryset):
        updated = queryset.update(completed=False)
        self.message_user(request, f'{updated} tareas marcadas como pendientes.')
    marcar_pendientes.short_description = '⏳ Marcar como pendientes'
    
    def cambiar_prioridad_alta(self, request, queryset):
        updated = queryset.update(prioridad='ALTA')
        self.message_user(request, f'{updated} tareas con prioridad ALTA.')
    cambiar_prioridad_alta.short_description = '🔥 Cambiar prioridad a ALTA'


# ============================================
# EVENTOS
# ============================================

@admin.register(Events)
class EventsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'titulo_display', 'category_badge', 'fecha', 
                    'hora', 'source_badge', 'user_link']
    list_filter = ['categoria', 'source', 'fecha']
    search_fields = ['titulo', 'descripcion', 'curso']
    readonly_fields = ['id', 'created_at', 'updated_at', 'tecsup_external_id']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información del Evento', {
            'fields': ('titulo', 'descripcion', 'curso')
        }),
        ('Fecha y Hora', {
            'fields': ('fecha', 'hora')
        }),
        ('Categoría', {
            'fields': ('categoria', 'source', 'sincronizado_tecsup', 'tecsup_external_id')
        }),
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Sistema', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def titulo_display(self, obj):
        icons = {
            'CLASE': '📚',
            'EXAMEN': '📝',
            'PERSONAL': '👤',
        }
        icon = icons.get(obj.categoria, '📅')
        return format_html(
            '{} <strong>{}</strong>',
            icon, obj.titulo
        )
    titulo_display.short_description = 'Título'
    
    def category_badge(self, obj):
        colors = {
            'CLASE': '#3b82f6',
            'EXAMEN': '#ef4444',
            'PERSONAL': '#10b981',
        }
        color = colors.get(obj.categoria, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: 700;">{}</span>',
            color, obj.categoria
        )
    category_badge.short_description = 'Categoría'
    
    def source_badge(self, obj):
        if obj.source == 'TECSUP':
            return format_html(
                '<span style="background: #3b82f6; color: white; padding: 4px 12px; '
                'border-radius: 12px; font-size: 11px; font-weight: 700;">🏫 TECSUP</span>'
            )
        return format_html(
            '<span style="color: #6b7280; font-size: 11px;">Manual</span>'
        )
    source_badge.short_description = 'Origen'
    
    def user_link(self, obj):
        if obj.user:
            return format_html(
                '<a href="/admin/dashboard/users/{}/change/" style="color: #667eea;">👤 {}</a>',
                obj.user.id, obj.user.name or obj.user.email
            )
        return format_html('<span style="color: #ef4444;">Sin usuario</span>')
    user_link.short_description = 'Usuario'


# ============================================
# HÁBITOS
# ============================================

@admin.register(Habits)
class HabitsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'nombre_display', 'tipo_badge', 'meta_diaria', 
                    'activo_badge', 'user_link']
    list_filter = ['tipo', 'activo', 'es_comida']
    search_fields = ['nombre']
    readonly_fields = ['id', 'created_at']
    
    fieldsets = (
        ('Información del Hábito', {
            'fields': ('nombre', 'tipo', 'meta_diaria')
        }),
        ('Estado', {
            'fields': ('activo', 'es_comida')
        }),
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Sistema', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def nombre_display(self, obj):
        icons = {
            'COMIDA': '🍽',
            'EJERCICIO': '💪',
            'SUEÑO': '😴',
            'AGUA': '💧',
            'OTRO': '⭐',
        }
        icon = icons.get(obj.tipo, '⭐')
        return format_html(
            '{} <strong>{}</strong>',
            icon, obj.nombre
        )
    nombre_display.short_description = 'Nombre'
    
    def tipo_badge(self, obj):
        colors = {
            'COMIDA': '#f59e0b',
            'EJERCICIO': '#10b981',
            'SUEÑO': '#8b5cf6',
            'AGUA': '#3b82f6',
            'OTRO': '#6b7280',
        }
        color = colors.get(obj.tipo, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: 700;">{}</span>',
            color, obj.tipo
        )
    tipo_badge.short_description = 'Tipo'
    
    def activo_badge(self, obj):
        if obj.activo:
            return format_html(
                '<span style="color: #10b981; font-weight: 700;">✅ Activo</span>'
            )
        return format_html(
            '<span style="color: #ef4444; font-weight: 700;">❌ Inactivo</span>'
        )
    activo_badge.short_description = 'Estado'
    
    def user_link(self, obj):
        if obj.user:
            return format_html(
                '<a href="/admin/dashboard/users/{}/change/" style="color: #667eea;">👤 {}</a>',
                obj.user.id, obj.user.name or obj.user.email
            )
        return format_html('<span style="color: #ef4444;">Sin usuario</span>')
    user_link.short_description = 'Usuario'


# ============================================
# PERSONALIZACIÓN DEL ADMIN SITE
# ============================================

admin.site.site_header = '🎓 EduSmart - Panel de Administración'
admin.site.site_title = 'EduSmart Admin'
admin.site.index_title = 'Gestión del Sistema'