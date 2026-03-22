from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from inscripciones.models import Inscripcion
from cursos.models import Curso
from accounts.utils import es_preceptor_o_director, es_preceptor
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

@login_required
@user_passes_test(es_preceptor_o_director)
def profesores_y_cursos(request):
    profesores = (
        User.objects
        .filter(groups__name='Profesor')
        .prefetch_related('cursos_dictados')  # related_name desde Curso
        .order_by('username')
    )

    return render(request, 'accounts/preceptor/profesores_y_cursos.html', {
        'profesores': profesores
    })

@login_required
@user_passes_test(es_preceptor_o_director)
def cursos_preceptor(request):
    cursos = Curso.objects.filter(activo=True).select_related('profesor')

    return render(request, 'accounts/preceptor/cursos.html', {
        'cursos': cursos
    })

@login_required
@user_passes_test(es_preceptor_o_director)
def alumnos_por_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    query = request.GET.get('q', '')

    inscripciones = (
        Inscripcion.objects
        .filter(curso=curso)
        .select_related('alumno')
    )

    if query:
        inscripciones = inscripciones.filter(
            Q(alumno__username__icontains=query) |
            Q(alumno__first_name__icontains=query) |
            Q(alumno__last_name__icontains=query) |
            Q(alumno__email__icontains=query)
        )

    inscripciones = inscripciones.order_by(
        'estado',
        'alumno__username'
    )

    return render(request, 'accounts/preceptor/alumnos_por_curso.html', {
        'curso': curso,
        'inscripciones': inscripciones,
        'query': query,
    })

@login_required
@user_passes_test(es_preceptor_o_director)
def listado_alumnos(request):
    query = request.GET.get('q', '')

    alumnos = User.objects.filter(
        groups__name='Alumno'
    )

    if query:
        alumnos = alumnos.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    alumnos = alumnos.order_by('last_name', 'first_name')

    return render(request, 'accounts/preceptor/listado_alumnos.html', {
        'alumnos': alumnos,
        'query': query
    })



@login_required
@user_passes_test(es_preceptor_o_director)
def ficha_academica_alumno(request, alumno_id):

    alumno = get_object_or_404(User, id=alumno_id)

    inscripcion = Inscripcion.objects.filter(
    alumno=alumno,
    curso__activo=True
).select_related('curso').first()

    return render(request, 'accounts/preceptor/ficha_academica_alumno.html', {
        'alumno': alumno,
        'inscripcion': inscripcion
    })

@login_required
@user_passes_test(es_preceptor_o_director)
def ficha_personal_alumno(request, alumno_id):

    alumno = get_object_or_404(User, id=alumno_id)

    inscripciones = (
        Inscripcion.objects
        .filter(alumno=alumno)
        .select_related('curso')
        
    )

    return render(request, 'accounts/preceptor/ficha_personal_alumno.html', {
        'alumno': alumno,
        'inscripciones': inscripciones
    })