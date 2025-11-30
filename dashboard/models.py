# dashboard/models.py
# Modelos Django conectados a la BD de Spring Boot (productivity_db)

from django.db import models


class Users(models.Model):
    """
    Modelo para usuarios
    Tabla: users (creada por Spring Boot)
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    preferences = models.JSONField(blank=True, null=True)
    tecsup_token = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def _str_(self):
        return f"{self.name} ({self.email})"


class Tasks(models.Model):
    """
    Modelo para tareas
    Tabla: tasks (creada por Spring Boot)
    """
    PRIORIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    ]

    id = models.BigAutoField(primary_key=True)
    completed = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='MEDIA')
    sincronizado_tecsup = models.BooleanField(blank=True, null=True, default=False)
    source = models.CharField(max_length=20, blank=True, null=True)
    tecsup_external_id = models.CharField(max_length=100, blank=True, null=True)
    titulo = models.CharField(max_length=250)
    updated_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tasks'
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-created_at']

    def _str_(self):
        return self.titulo


class Events(models.Model):
    """
    Modelo para eventos
    Tabla: events (creada por Spring Boot)
    """
    CATEGORIA_CHOICES = [
        ('CLASE', 'Clase'),
        ('EXAMEN', 'Examen'),
        ('PERSONAL', 'Personal'),
    ]

    id = models.BigAutoField(primary_key=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    created_at = models.DateTimeField(blank=True, null=True)
    curso = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField(blank=True, null=True)
    sincronizado_tecsup = models.BooleanField(blank=True, null=True, default=False)
    source = models.CharField(max_length=20, blank=True, null=True)
    tecsup_external_id = models.CharField(max_length=100, blank=True, null=True)
    titulo = models.CharField(max_length=250)
    updated_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'events'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha', 'hora']

    def _str_(self):
        return f"{self.titulo} - {self.fecha}"


class Habits(models.Model):
    """
    Modelo para hábitos
    Tabla: habits (creada por Spring Boot)
    """
    TIPO_CHOICES = [
        ('COMIDA', 'Comida'),
        ('EJERCICIO', 'Ejercicio'),
        ('SUEÑO', 'Sueño'),
        ('AGUA', 'Agua'),
        ('OTRO', 'Otro'),
    ]

    id = models.BigAutoField(primary_key=True)
    activo = models.BooleanField(blank=True, null=True, default=True)
    created_at = models.DateTimeField(blank=True, null=True)
    es_comida = models.BooleanField(blank=True, null=True, default=False)
    meta_diaria = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    user = models.ForeignKey(Users, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'habits'
        verbose_name = 'Hábito'
        verbose_name_plural = 'Hábitos'
        ordering = ['-created_at']

    def _str_(self):
        return self.nombre