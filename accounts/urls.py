from django.urls import path
from accounts.views.preceptor import (cursos_preceptor, alumnos_por_curso, profesores_y_cursos,ficha_academica_alumno, listado_alumnos, ficha_personal_alumno)


urlpatterns = [
    path(
        'preceptor/cursos/',
        cursos_preceptor,
        name='preceptor_cursos'
    ),
    path(
        'preceptor/cursos/<int:curso_id>/alumnos/',
        alumnos_por_curso,
        name='preceptor_alumnos_por_curso'
    ),

    path(
        'preceptor/profesores/',
        profesores_y_cursos,
        name='preceptor_profesores'
    ),

    path(
        'preceptor/alumnos/',
        listado_alumnos,
        name='preceptor_alumnos'
    ),


    path(
        'preceptor/alumno/<int:alumno_id>/',
        ficha_academica_alumno,
        name='preceptor_ficha_alumno'
    ),
    path(
    'preceptor/alumno_personal/<int:alumno_id>/',
    ficha_personal_alumno,
    name='ficha_personal'
),
]