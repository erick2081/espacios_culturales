from django.db import models
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.storage import default_storage

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
    NOTIFICAR_CHOICES = [
        ('SI', 'Sí'),
        ('NO', 'No'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='evaluaciones')
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha = models.DateField(auto_now_add=True)
    puntuacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Correo electrónico")
    notificar = models.CharField(
        max_length=2, 
        choices=NOTIFICAR_CHOICES, 
        default='NO', 
        verbose_name="Notificar"
    )
    
    def save(self, *args, **kwargs):
        # Verificar si se selecciona "Sí" en notificar y si existe un correo electrónico
        if self.notificar == 'SI' and self.email:
            # Crear el mensaje de correo
            subject = "Notificación de Evaluación"
            message = (
                f"Estimado/a {self.cliente.nombre},\n\n"  # Accediendo al nombre del cliente
                f"Le informamos que hemos recibido su evaluación para el espacio: {self.espacio.nombre}.\n\n"
                f"Puntuación: {self.puntuacion}.\n\n"
                f"Comentario: {self.comentario or 'Sin comentarios'}.\n\n"
                "Gracias por su participación.\n\nAtentamente,\nEl equipo de evaluaciones."
            )

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Usa la configuración de correo por defecto
                to=[self.email],  # Correo del cliente
            )
            
            
            # Enviar el correo
            try:
                email.send(fail_silently=False)
            except Exception as e:
                print(f"Error al enviar el correo: {e}")

        # Llamada al método save original para guardar el objeto en la base de datos
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.espacio.nombre} ({self.puntuacion})"
    
