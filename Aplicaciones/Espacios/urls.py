from django.urls import path, include
from . import views                                                                                                                
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView  # Importación correcta
from .views import LoginView, register, home, inicio # Importamos solo lo necesario

urlpatterns = [
    path('', inicio, name='inicio'),  # Página de inicio
    path('home/', home, name='home'),  # Página principal autenticada
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    ###########################################################################################

    path('cliente_crear/', views.cliente_crear, name='cliente_crear'),
    path('cliente_mostrar/', views.cliente_mostrar, name='cliente_mostrar'),
    path('cliente_editar/<int:id>/', views.cliente_editar, name='cliente_editar'),
    path('guardar_cliente/', views.guardar_cliente, name='guardar_cliente'),
    path('eliminar_cliente/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

#############################################################################################
    path('espacio_crear/', views.espacio_crear, name='espacio_crear'),
    path('espacio_mostrar/', views.espacio_mostrar, name='espacio_mostrar'),
    path('espacio_editar/<int:id>/', views.espacio_editar, name='espacio_editar'),
    path('guardar_espacio/', views.guardar_espacio, name='guardar_espacio'),
    path('eliminar_espacio/<int:id>/', views.eliminar_espacio, name='eliminar_espacio'),
#############################################################################################

    path('proyecto_crear/', views.proyecto_crear, name='proyecto_crear'),
    path('proyecto_mostrar/', views.proyecto_mostrar, name='proyecto_mostrar'),
    path('proyecto_editar/<int:id>/', views.proyecto_editar, name='proyecto_editar'),
    path('guardar_proyecto/', views.guardar_proyecto, name='guardar_proyecto'),
    path('eliminar_proyecto/<int:id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
##########################################################################################################

    path('evaluacion_crear/', views.evaluacion_crear, name='evaluacion_crear'),
    path('evaluacion_mostrar/', views.evaluacion_mostrar, name='evaluacion_mostrar'),
    path('evaluacion_editar/<int:id>/', views.evaluacion_editar, name='evaluacion_editar'),
    path('guardar_evaluacion/', views.agregar_evaluacion, name='agregar_evaluacion'),
    path('eliminar_evaluacion/<int:id>/', views.eliminar_evaluacion, name='eliminar_evaluacion'),

]

# Manejo de archivos estáticos y media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)