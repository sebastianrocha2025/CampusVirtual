from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from cursos.models import Curso
from .models import Inscripcion
from accounts.utils import es_alumno


@login_required
@user_passes_test(es_alumno)
def inscribirse(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, activo=True)

    # 1️⃣ Evitar doble inscripción
    if Inscripcion.objects.filter(
        alumno=request.user,
        curso=curso,
        estado='activo'
    ).exists():
        return redirect('lista_cursos')

    # 2️⃣ Validar cupo
    if not curso.tiene_cupo():
        return redirect('lista_cursos')

    # 3️⃣ Crear inscripción
    Inscripcion.objects.create(
        alumno=request.user,
        curso=curso,
        estado='activo'
    )

    return redirect('lista_cursos')
