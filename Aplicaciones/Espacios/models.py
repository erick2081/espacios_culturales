from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=10, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Espacio(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.TextField()
    capacidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='espacio/', blank=True, null=True, )
    
    def __str__(self):
        return self.nombre

class ProyectoConstruccion(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, related_name='proyectos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='proyectos')
    estado = models.CharField(max_length=50, choices=[('En progreso', 'En progreso'), ('Finalizado', 'Finalizado'), ('Cancelado', 'Cancelado')])
    
    def __str__(self):
        return self.nombre

class Evaluacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='evaluaciones')
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha = models.DateField(auto_now_add=True)
    puntuacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.cliente.nombre} - {self.espacio.nombre} ({self.puntuacion})"
