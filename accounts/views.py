from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from inscripciones.models import Inscripcion
from accounts.utils import es_preceptor


@login_required
@user_passes_test(es_preceptor)
def listado_alumnos_preceptor(request):
    inscripciones = (
        Inscripcion.objects
        .select_related('alumno', 'curso', 'curso__profesor')
        .order_by('curso__nombre', 'alumno__username')
    )

    return render(request, 'preceptor/listado_alumnos.html', {
        'inscripciones': inscripciones
    })

