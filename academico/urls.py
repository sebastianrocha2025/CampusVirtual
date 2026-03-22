from django.urls import path, include
from . import views

urlpatterns = [

    # 📄 Ficha académica del alumno (profesor)
    path(
        'profesor/inscripcion/<int:inscripcion_id>/',
        views.detalle_inscripcion_profesor,
        name='profesor_detalle_inscripcion'
    ),

    # ➕ Cargar nota
    path(
        'profesor/inscripcion/<int:inscripcion_id>/nota/nueva/',
        views.cargar_nota,
        name='profesor_cargar_nota'
    ),

    # ✏️ Editar / borrar nota
    # path(
    #     'profesor/nota/<int:nota_id>/editar/',
    #     views.editar_nota,
    #     name='profesor_editar_nota'
    # ),
    # path(
    #     'profesor/nota/<int:nota_id>/eliminar/',
    #     views.eliminar_nota,
    #     name='profesor_eliminar_nota'
    # ),




    path(
    'profesor/curso/<int:curso_id>/asistencia/',
    views.profesor_tomar_asistencia,
    name='profesor_tomar_asistencia'
),
   path(
    'profesor/curso/<int:curso_id>/asistencia/editar/',
    views.profesor_editar_asistencia,
    name='profesor_editar_asistencia'
),


    path("profesor/", include("academico.urls_profesor")),
     path(
    'alumno/cuestionario/<int:cuestionario_id>/',
    views.alumno_responder_cuestionario,
    name='alumno_responder_cuestionario'
),

path(
    "profesor/cuestionario/<int:cuestionario_id>/entregas/",
    views.profesor_entregas_cuestionario,
    name="profesor_entregas_cuestionario"
),

path(
    "profesor/curso/<int:curso_id>/notas/",
    views.profesor_notas_curso,
    name="profesor_notas_curso"
),

]

