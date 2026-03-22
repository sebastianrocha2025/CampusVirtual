from django.urls import path
from . import views
from .views import lista_cursos, profesor_detalle_inscripcion, progreso_academico, material_clase
urlpatterns = [
    # ----------------------
    # GENERALES
    # ----------------------
    
    path('lista-cursos/', lista_cursos, name='lista_cursos'),
    path('mis-cursos/', views.mis_cursos, name='mis_cursos'),

    # ----------------------
    # VISTAS DEL ALUMNO
    # ----------------------

    
    path(
    'alumno/curso/<int:curso_id>/progreso/',
    views.progreso_academico,
    name='progreso_academico'),

    path(
    'alumno/curso/<int:curso_id>/material/',
    views.material_clase,
    name='material_clase'),



    # ----------------------
    # VISTAS DEL PROFESOR
    # ----------------------
    path('profesor/cursos/', views.cursos_profesor, name='cursos_profesor'),

    path(
        'profesor/curso/<int:curso_id>/',
        views.detalle_curso_profesor,
        name='profesor_detalle_curso'
    ),

    path(
        'profesor/inscripcion/<int:inscripcion_id>/',
        views.profesor_detalle_inscripcion,
        name='profesor_detalle_inscripcion'
    ),

    path(
        'profesor/inscripcion/<int:inscripcion_id>/nota/nueva/',
        views.profesor_cargar_nota,
        name='profesor_cargar_nota'
    ),

    path(
        'profesor/nota/<int:nota_id>/editar/',
        views.profesor_editar_nota,
        name='profesor_editar_nota'
    ),

    path(
        'profesor/nota/<int:nota_id>/borrar/',
        views.profesor_borrar_nota,
        name='profesor_borrar_nota'
    ),

    path(
        'profesor/asistencia/<int:asistencia_id>/editar/',
        views.profesor_editar_asistencia,
        name='profesor_editar_asistencia'
    ),

    path(
        'profesor/asistencia/<int:asistencia_id>/borrar/',
        views.profesor_borrar_asistencia,
        name='profesor_borrar_asistencia'
    ),
]