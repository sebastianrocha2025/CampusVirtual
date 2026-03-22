from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import es_profesor
from inscripciones.models import Inscripcion, Curso
from .models import Nota, Asistencia
from .forms import NotaForm, AsistenciaForm
from django.db.models import DateField, Q, Count
from django.db.models.functions import Cast
from datetime import date
from .forms import NotaForm
from django.contrib import messages
from academico.models import (
    Cuestionario, EntregaCuestionario,
    RespuestaOpcion, Inscripcion, Nota
)
from collections import defaultdict
from django.utils import timezone



@login_required
@user_passes_test(es_profesor)
def detalle_inscripcion_profesor(request, inscripcion_id):
    inscripcion = get_object_or_404(
        Inscripcion,
        id=inscripcion_id,
        curso__profesor=request.user  # 🔐 CLAVE DE SEGURIDAD
    )

    return render(request, 'academico/profesor/profesor_detalle_inscripcion.html', {
        'inscripcion': inscripcion,
        'notas': inscripcion.notas.all(),
        'asistencias': inscripcion.asistencias.all(),
    })

@login_required
@user_passes_test(es_profesor)
def cargar_nota(request, inscripcion_id):
    inscripcion = get_object_or_404(
        Inscripcion,
        id=inscripcion_id,
        curso__profesor=request.user
    )

    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.inscripcion = inscripcion
            nota.save()

            messages.success(request, '✅ Nota cargada correctamente.')
            return redirect(
                'profesor_detalle_inscripcion',
                inscripcion_id=inscripcion.id
            )
        else:
            messages.error(request, '❌ Error al cargar la nota.')
    else:
        form = NotaForm()

    return render(request, 'academico/profesor/profesor_cargar_nota.html', {
        'form': form,
        'inscripcion': inscripcion
    })

@login_required
@user_passes_test(es_profesor)
def profesor_tomar_asistencia(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, profesor=request.user)

    inscripciones = (
        Inscripcion.objects
        .filter(curso=curso, estado=Inscripcion.ACTIVO)
        .prefetch_related('asistencias')
    )

    fechas = (
        Asistencia.objects
        .filter(inscripcion__curso=curso)
        .values_list('fecha', flat=True)
        .distinct()
        .order_by('fecha')
    )

    fecha_hoy = date.today()

    if request.method == 'POST':
        for inscripcion in inscripciones:
            presente = request.POST.get(
                f'presente_{inscripcion.id}'
            ) == 'on'

            Asistencia.objects.update_or_create(
                inscripcion=inscripcion,
                fecha=fecha_hoy,
                defaults={'presente': presente}
            )

        messages.success(request, 'Asistencia guardada correctamente.')
        return redirect('profesor_tomar_asistencia', curso.id)

    return render(request, 'academico/tomar_asistencia.html', {
        'curso': curso,
        'inscripciones': inscripciones,
        'fechas': fechas,
        'fecha_hoy': fecha_hoy,
    })
 
@login_required
@user_passes_test(es_profesor)
def profesor_editar_asistencia(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id, profesor=request.user)

    inscripciones = (
        Inscripcion.objects
        .filter(curso=curso, estado=Inscripcion.ACTIVO)
        .prefetch_related("asistencias")
    )

    fechas = (
        Asistencia.objects
        .filter(inscripcion__curso=curso)
        .values_list("fecha", flat=True)
        .distinct()
        .order_by("fecha")
    )

    if request.method == "POST":
        for inscripcion in inscripciones:
            for fecha in fechas:
                key = f"asistencia_{inscripcion.id}_{fecha}"
                valor = request.POST.get(key)

                if valor not in ("P", "A"):
                    continue

                Asistencia.objects.update_or_create(
                    inscripcion=inscripcion,
                    fecha=fecha,
                    defaults={"presente": valor == "P"}
                )

        messages.success(request, "Historial actualizado correctamente.")
        return redirect("profesor_editar_asistencia", curso.id)

    # 🔹 MAPA LIMPIO (la clave del éxito)
    asistencias_map = {}
    for inscripcion in inscripciones:
        asistencias_map[inscripcion.id] = {}
        for a in inscripcion.asistencias.all():
            asistencias_map[inscripcion.id][a.fecha] = a.presente

    return render(request, "academico/editar_asistencia.html", {
        "curso": curso,
        "inscripciones": inscripciones,
        "fechas": fechas,
        "asistencias_map": asistencias_map,
    })




def alumno_responder_cuestionario(request, cuestionario_id):

    cuestionario = get_object_or_404(Cuestionario, id=cuestionario_id)
    curso = cuestionario.clase.curso

    inscripcion = get_object_or_404(
        Inscripcion,
        alumno=request.user,
        curso=curso
    )

    preguntas = cuestionario.preguntas.prefetch_related("opciones")

    # 🔒 Verificar si ya entregó
    entrega_existente = EntregaCuestionario.objects.filter(
        cuestionario=cuestionario,
        inscripcion=inscripcion
    ).first()

    if entrega_existente:
        return render(request, "alumno/cuestionario_ya_entregado.html", {
            "cuestionario": cuestionario
        })

    if request.method == "POST":

        entrega = EntregaCuestionario.objects.create(
            cuestionario=cuestionario,
            inscripcion=inscripcion
        )

        for pregunta in preguntas:
            opciones_ids = request.POST.getlist(f"pregunta_{pregunta.id}")

            for opcion_id in opciones_ids:
                RespuestaOpcion.objects.create(
                    entrega=entrega,
                    opcion_id=opcion_id
                )

        # 🔥 Calcular nota
        respuestas = entrega.respuestas.select_related("opcion")

        correctas = sum(
            1 for r in respuestas if r.opcion.es_correcta
        )

        total = cuestionario.preguntas.count()
        nota_final = (correctas / total) * 10 if total > 0 else 0

        Nota.objects.update_or_create(
            inscripcion=inscripcion,
            cuestionario=cuestionario,
            defaults={
                "valor": round(nota_final, 2)
            }
        )

        return redirect("alumno_responder_cuestionario", cuestionario.id)

    return render(request, "alumno/responder_cuestionario.html", {
        "cuestionario": cuestionario,
        "preguntas": preguntas
    })

@login_required
def profesor_entregas_cuestionario(request, cuestionario_id):

    cuestionario = get_object_or_404(Cuestionario, id=cuestionario_id)

    if cuestionario.clase.curso.profesor != request.user:
        return redirect("home")

    curso = cuestionario.clase.curso

    inscripciones = Inscripcion.objects.filter(
        curso=curso
    ).select_related("alumno")

    entregas = EntregaCuestionario.objects.filter(
        cuestionario=cuestionario
    ).select_related("inscripcion__alumno")

    entregas_dict = {
        entrega.inscripcion.id: entrega
        for entrega in entregas
    }

    data = []
    total_preguntas = cuestionario.preguntas.count()

    for inscripcion in inscripciones:

        entrega = entregas_dict.get(inscripcion.id)
        puntaje = None

        if entrega:
            respuestas = entrega.respuestas.select_related("opcion")

            correctas = sum(
                1 for r in respuestas if r.opcion.es_correcta
            )

            puntaje = f"{correctas} / {total_preguntas}"

        data.append({
            "alumno": inscripcion.alumno,
            "entrega": entrega,
            "puntaje": puntaje
        })

    return render(request, "academico/profesor_entregas.html", {
        "cuestionario": cuestionario,
        "data": data
    })


def profesor_notas_curso(request, curso_id):

    curso = get_object_or_404(Curso, id=curso_id)

    if curso.profesor != request.user:
        return redirect("home")

    cuestionarios = Cuestionario.objects.filter(
        clase__curso=curso
    )

    inscripciones = Inscripcion.objects.filter(
        curso=curso
    ).select_related("alumno")

    notas = Nota.objects.filter(
        inscripcion__curso=curso,
        cuestionario__isnull=False
    ).select_related("inscripcion", "cuestionario")

    # Diccionario: {inscripcion_id: {cuestionario_id: valor}}
    notas_dict = defaultdict(dict)

    for nota in notas:
        notas_dict[nota.inscripcion_id][nota.cuestionario_id] = nota.valor

    tabla = []

    for inscripcion in inscripciones:

        fila = {
            "alumno": inscripcion.alumno,
            "notas": []
        }

        for cuestionario in cuestionarios:
            valor = notas_dict[inscripcion.id].get(cuestionario.id)
            fila["notas"].append(valor)

        tabla.append(fila)

    return render(request, "academico/profesor_notas_curso.html", {
        "curso": curso,
        "cuestionarios": cuestionarios,
        "tabla": tabla
    })