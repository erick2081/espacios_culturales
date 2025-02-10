from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Cliente, Espacio, ProyectoConstruccion, Evaluacion


# Vista de inicio para usuarios autenticados
@login_required
def home(request):
    return render(request, 'home.html')


# Vista de login
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        return render(request, self.template_name, {'form': form})


# Vista de logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Has cerrado sesión.")
        return redirect('login')


# Vista de registro
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Registro exitoso. ¡Bienvenido!')
                return redirect('login')
        else:
            messages.error(request, "Errores al registrar el usuario.")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


# Vista principal
def inicio(request):
    return render(request, 'inicio.html')


##################################################################################################################################
# Funciones CRUD para el cliente
# Crear cliente

def cliente_crear(request):
    return render(request, 'cliente_crear.html')

# Guardar cliente
def guardar_cliente(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        try:
            Cliente.objects.create(
                cedula=cedula,
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion
            )
            messages.success(request, "¡Cliente guardado exitosamente!")
            return redirect('cliente_mostrar')
        except Exception as e:
            messages.error(request, f"Error al guardar el cliente: {e}")
    
    return render(request, 'cliente_crear.html')


# Mostrar listado de clientes
def cliente_mostrar(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente_mostrar.html', {'clientes': clientes})


# Editar cliente
def cliente_editar(request, id):
    cliente = get_object_or_404(Cliente, id=id)  # Asegúrate de usar el modelo correcto

    if request.method == 'POST':
        cliente.cedula = request.POST.get('cedula')
        cliente.nombre = request.POST.get('nombre')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')

        try:
            cliente.save()
            messages.success(request, "¡Cliente actualizado exitosamente!")
            return redirect('/cliente_mostrar/')
        except Exception as e:
            messages.error(request, f"Error al actualizar el cliente: {e}")

    return render(request, 'cliente_editar.html', {'cliente': cliente})



# Eliminar cliente
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, "¡Cliente eliminado exitosamente!")
    return redirect('cliente_mostrar')

########################################################################################################

# Crear espacio
def espacio_crear(request):
    return render(request, 'espacio_crear.html')

# Guardar espacio
def guardar_espacio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ubicacion = request.POST.get('ubicacion')
        capacidad = request.POST.get('capacidad')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen', None)

        try:
            Espacio.objects.create(
                nombre=nombre,
                ubicacion=ubicacion,
                capacidad=capacidad,
                descripcion=descripcion,
                imagen=imagen
            )
            messages.success(request, "¡Espacio guardado exitosamente!")
            return redirect('espacio_mostrar')
        except Exception as e:
            messages.error(request, f"Error al guardar el espacio: {e}")
    
    return render(request, 'espacio_crear.html')

# Mostrar listado de espacios
def espacio_mostrar(request):
    espacios = Espacio.objects.all()
    return render(request, 'espacio_mostrar.html', {'espacios': espacios})

# Editar espacio
def espacio_editar(request, id):
    espacio = get_object_or_404(Espacio, id=id)

    if request.method == 'POST':
        espacio.nombre = request.POST.get('nombre')
        espacio.ubicacion = request.POST.get('ubicacion')
        espacio.capacidad = request.POST.get('capacidad')
        espacio.descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen', None)
        if imagen:
            espacio.imagen = imagen

        try:
            espacio.save()
            messages.success(request, "¡Espacio actualizado exitosamente!")
            return redirect('/espacio_mostrar/')
        except Exception as e:
            messages.error(request, f"Error al actualizar el espacio: {e}")

    return render(request, 'espacio_editar.html', {'espacio': espacio})

# Eliminar espacio
def eliminar_espacio(request, id):
    espacio = get_object_or_404(Espacio, id=id)
    espacio.delete()
    messages.success(request, "¡Espacio eliminado exitosamente!")
    return redirect('espacio_mostrar')

##################################################################################################

# Crear proyecto
def proyecto_crear(request):
    clientes = Cliente.objects.all()
    espacios = Espacio.objects.all()
    return render(request, 'proyecto_crear.html', {'clientes': clientes,'espacios': espacios})

# Listado de proyectos
def proyecto_mostrar(request):
    proyectos = ProyectoConstruccion.objects.all()
    return render(request, 'proyecto_mostrar.html', {'proyectos': proyectos})

# Editar proyecto
def proyecto_editar(request, id):
    proyecto = get_object_or_404(ProyectoConstruccion, id=id)
    espacios = Espacio.objects.all()
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        proyecto.nombre = request.POST.get('nombre')
        proyecto.fecha_inicio = request.POST.get('fecha_inicio')
        proyecto.fecha_fin = request.POST.get('fecha_fin') or None
        proyecto.presupuesto = request.POST.get('presupuesto')
        proyecto.espacio_id = request.POST.get('espacio')
        proyecto.cliente_id = request.POST.get('cliente')
        proyecto.estado = request.POST.get('estado')

        try:
            proyecto.save()
            messages.success(request, "¡Proyecto actualizado exitosamente!")
            return redirect('proyecto_mostrar') 
        except Exception as e:
            messages.error(request, f"Error al actualizar el proyecto: {e}")

    return render(request, 'proyecto_editar.html', {
        'proyecto': proyecto,
        'espacios': espacios,
        'clientes': clientes
    })




# Guardar proyecto
def guardar_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        presupuesto = request.POST.get('presupuesto')
        espacio_id = request.POST.get('espacio')
        cliente_id = request.POST.get('cliente')
        estado = request.POST.get('estado')

        try:
            espacio = Espacio.objects.get(id=espacio_id)
            cliente = Cliente.objects.get(id=cliente_id)
            
            ProyectoConstruccion.objects.create(
                nombre=nombre,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                presupuesto=presupuesto,
                espacio=espacio,
                cliente=cliente,
                estado=estado
            )
            messages.success(request, "¡Proyecto guardado exitosamente!")
            return redirect('proyecto_mostrar')
        except Exception as e:
            messages.error(request, f"Error al guardar el proyecto: {e}")
    
    return redirect('proyecto_crear')

# Eliminar proyecto
def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(ProyectoConstruccion, id=id)

    try:
        proyecto.delete()
        messages.success(request, "¡Proyecto eliminado exitosamente!")
    except Exception as e:
        messages.error(request, f"Error al eliminar proyecto: {e}")

    return redirect('/proyecto_mostrar/')

##################################################################################################
# Crear evalucion
def evaluacion_crear(request):
    clientes = Cliente.objects.all()
    espacios = Espacio.objects.all()
    return render(request, 'evaluacion_crear.html', {'clientes': clientes,'espacios': espacios})

# Listado de evaluacion
def evaluacion_mostrar(request):
    evaluaciones = Evaluacion.objects.all()
    return render(request, 'evaluacion_mostrar.html', {'evaluaciones': evaluaciones})


#
def agregar_evaluacion(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        espacio_id = request.POST.get('espacio')
        fecha = request.POST.get('fecha')
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario')

        cliente = Cliente.objects.get(id=cliente_id)
        espacio = Espacio.objects.get(id=espacio_id)

        Evaluacion.objects.create(
            cliente=cliente,
            espacio=espacio,
            fecha=fecha,
            puntuacion=puntuacion,
            comentario=comentario
        )

        messages.success(request, "Evaluación guardada correctamente.")
        return redirect('evaluacion_mostrar')

    clientes = Cliente.objects.all()
    espacios = Espacio.objects.all()
    
    return render(request, 'evaluacion_crear.html', {
        'clientes': clientes,
        'espacios': espacios
    })
### editar
def evaluacion_editar(request,id):
    evaluacion = get_object_or_404(Evaluacion, id=id)
    clientes = Cliente.objects.all()
    espacios = Espacio.objects.all()
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        espacio_id = request.POST.get('espacio')
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario', '').strip()
        
        if not cliente_id or not espacio_id or not puntuacion:
            messages.error(request, "Todos los campos obligatorios deben ser completados.")
        else:
            evaluacion.cliente_id = cliente_id
            evaluacion.espacio_id = espacio_id
            evaluacion.puntuacion = int(puntuacion)
            evaluacion.comentario = comentario if comentario else None
            evaluacion.save()
            messages.success(request, "Evaluación actualizada correctamente.")
            return redirect('evaluacion_mostrar')
    
    return render(request, 'evaluacion_editar.html', {
        'evaluacion': evaluacion,
        'clientes': clientes,
        'espacios': espacios
    })

# Eliminar proyecto
def eliminar_evaluacion(request, id):
    evaluacion = get_object_or_404(Evaluacion, id=id)
    
    try:
        evaluacion.delete()
        messages.success(request, "Evaluación eliminada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la evaluación: {str(e)}")
    
    return redirect('/evaluacion_mostrar/')