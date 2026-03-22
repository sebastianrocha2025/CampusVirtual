from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Curso
from inscripciones.models import Inscripcion
from accounts.utils import es_alumno, es_profesor
from academico.forms import NotaForm, AsistenciaForm
from academico.models import Nota, Asistencia
from django.contrib import messages
from academico.models import Clase, Cuestionario, MaterialClase

def home(request):
    return redirect('home')

def lista_cursos(request):
    # 🚫 Si es profesor, NO usa esta vista
    if request.user.is_authenticated and es_profesor(request.user):
        return redirect('cursos_profesor')

    # 👨‍🎓 Alumno o anónimo
    cursos = Curso.objects.filter(activo=True)

    user_es_alumno = (
        request.user.is_authenticated and es_alumno(request.user)
    )

    cursos_con_estado = []
    for curso in cursos:
        inscripto = False
        if user_es_alumno:
            inscripto = curso.alumno_inscripto(request.user)

        cursos_con_estado.append({
            'curso': curso,
            'inscripto': inscripto,
        })

    return render(request, 'cursos/lista_cursos.html', {
        'cursos_con_estado': cursos_con_estado,
        'es_alumno': user_es_alumno,
    })


@login_required
@user_passes_test(es_alumno)
def mis_cursos(request):
    inscripciones = (
        Inscripcion.objects
        .filter(alumno=request.user, estado=Inscripcion.ACTIVO)
        .select_related('curso')
    )

    return render(request, 'cursos/mis_cursos.html', {
        'inscripciones': inscripciones
    })


@login_required
@user_passes_test(es_profesor)
def cursos_profesor(request):
    cursos = Curso.objects.filter(profesor=request.user)

    return render(request, 'cursos/profesor_cursos.html', {
        'cursos': cursos
    })


@login_required
@user_passes_test(es_profesor)
def detalle_curso_profesor(request, curso_id):
    curso = get_object_or_404(
        Curso,
        id=curso_id,
        profesor=request.user
    )

    inscripciones = (
        Inscripcion.objects
        .filter(curso=curso, estado=Inscripcion.ACTIVO)
        .select_related('alumno')
    )

    return render(request, 'cursos/profesor_detalle_curso.html', {
        'curso': curso,
        'inscripciones': inscripciones
    })


@login_required
@user_passes_test(es_profesor)
def profesor_detalle_inscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(
        Inscripcion,
        id=inscripcion_id,
        curso__profesor=request.user  # 🔐 seguridad CLAVE
    )

    notas = inscripcion.notas.all()
    asistencias = inscripcion.asistencias.all()

    return render(request, 'academico/profesor/profesor_detalle_inscripcion.html', {
        'inscripcion': inscripcion,
        'notas': notas,
        'asistencias': asistencias,
    })

@login_required
@user_passes_test(es_profesor)
def profesor_cargar_nota(request, inscripcion_id):


    inscripcion = get_object_or_404(
        Inscripcion,
        id=inscripcion_id,
        curso__profesor=request.user  # 🔐 seguridad clave
    )

    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.inscripcion = inscripcion
            nota.save()
            return redirect(
                'profesor_detalle_inscripcion',
                inscripcion_id=inscripcion.id
            )
    else:
        form = NotaForm()

    return render(request, 'cursos/profesor_cargar_nota.html', {
        'form': form,
        'inscripcion': inscripcion
    })

@login_required
@user_passes_test(es_profesor)
def profesor_editar_nota(request, nota_id):
    nota = get_object_or_404(
        Nota,
        id=nota_id,
        inscripcion__curso__profesor=request.user  # 🔐 clave
    )

    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ La nota fue modificada correctamente.')
            return redirect(
                'profesor_detalle_inscripcion',
                inscripcion_id=nota.inscripcion.id
            )
    else:
        form = NotaForm(instance=nota)

    return render(request, 'cursos/profesor_editar_nota.html', {
        'form': form,
        'nota': nota
    })

@login_required
@user_passes_test(es_profesor)
def profesor_borrar_nota(request, nota_id):
    nota = get_object_or_404(
        Nota,
        id=nota_id,
        inscripcion__curso__profesor=request.user
    )

    inscripcion_id = nota.inscripcion.id
    nota.delete()

    messages.success(request, '🗑 La nota fue eliminada correctamente.')

    return redirect(
        'profesor_detalle_inscripcion',
        inscripcion_id=inscripcion_id
    )



@login_required
@user_passes_test(es_profesor)
def profesor_editar_asistencia(request, asistencia_id):
    asistencia = get_object_or_404(
        Asistencia,
        id=asistencia_id,
        inscripcion__curso__profesor=request.user
    )

    if request.method == 'POST':
        form = AsistenciaForm(request.POST, instance=asistencia)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Asistencia modificada.')
            return redirect(
                'profesor_detalle_inscripcion',
                inscripcion_id=asistencia.inscripcion.id
            )
    else:
        form = AsistenciaForm(instance=asistencia)

    return render(request, 'cursos/profesor_editar_asistencia.html', {
        'form': form,
        'asistencia': asistencia
    })

@login_required
@user_passes_test(es_profesor)
def profesor_borrar_asistencia(request, asistencia_id):

    asistencia = get_object_or_404(
        Asistencia,
        id=asistencia_id,
        inscripcion__curso__profesor=request.user
    )

    inscripcion_id = asistencia.inscripcion.id
    asistencia.delete()

    messages.success(request, '🗑 Asistencia eliminada.')

    return redirect(
        'profesor_detalle_inscripcion',
        inscripcion_id=inscripcion_id
    )

def progreso_academico(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    alumno = request.user

    # 🔹 Obtenemos la inscripción del alumno en ese curso
    inscripcion = get_object_or_404(
        Inscripcion,
        curso=curso,
        alumno=alumno
    )

    # 🔹 Ahora todo se filtra por inscripción
    asistencias = inscripcion.asistencias.all()
    notas = inscripcion.notas.all()

    return render(request, "alumno/progreso.html", {
        "curso": curso,
        "inscripcion": inscripcion,
        "asistencias": asistencias,
        "notas": notas
    })
def material_clase(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    clases = Clase.objects.filter(curso=curso)

    cuestionarios = Cuestionario.objects.filter(
        clase__curso=curso,
        activo=True
    )

    return render(request, "alumno/material.html", {
        "curso": curso,
        "clases": clases,
        "cuestionarios": cuestionarios
    })