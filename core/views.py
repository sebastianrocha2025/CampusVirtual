from django.shortcuts import render, redirect
from .forms import SolicitudInscripcionForm
from django.contrib import messages
from django.core.mail import send_mail


def home(request):

    if request.user.is_authenticated:

        user = request.user

        if user.groups.filter(name='Director').exists():
            return redirect('preceptor_cursos')

        if user.groups.filter(name='Profesor').exists():
            return redirect('lista_cursos')

        if user.groups.filter(name='Preceptor').exists():
            return redirect('preceptor_cursos')

        if user.groups.filter(name='Alumno').exists():
            return redirect('lista_cursos')

    return render(request, 'home.html')





def solicitud_inscripcion(request):

    if request.method == 'POST':
        form = SolicitudInscripcionForm(request.POST)

        if form.is_valid():
            solicitud = form.save()

            # enviar email a administración
            send_mail(
                'Nueva solicitud de inscripción',
                f'''
Nombre: {solicitud.nombre}
DNI: {solicitud.dni}
Fecha nacimiento: {solicitud.fecha_nacimiento}
Celular: {solicitud.celular}
Email: {solicitud.email}
Curso: {solicitud.curso_interes}
Mensaje: {solicitud.mensaje}
''',
                'idfyc_2026@gmail.com',
                ['idfyc_2026@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, 'Solicitud enviada correctamente')
            return redirect('home')

    else:
        form = SolicitudInscripcionForm()

    return render(request, 'core/solicitud_inscripcion.html', {'form': form})