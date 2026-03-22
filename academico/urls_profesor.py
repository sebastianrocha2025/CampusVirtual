from django.urls import path
from . import views_profesor

app_name = "profesor"

urlpatterns = [

    # ===== CLASES =====
    path("clases/", views_profesor.profesor_clases, name="clases"),


    path(
        'profesor/cursos/<int:curso_id>/clases/nueva/',
        views_profesor.profesor_clase_crear,
        name='profesor_clase_crear'
    ),


    path("clases/<int:clase_id>/editar/", views_profesor.profesor_clase_editar, name="profesor_clase_editar"),
    
    path(
    "cursos/<int:curso_id>/clases/",
    views_profesor.profesor_clases_por_curso,
    name="profesor_clases_por_curso"
),


    # ===== CUESTIONARIOS =====
    path(
        "clases/<int:clase_id>/cuestionarios/",
        views_profesor.profesor_cuestionarios,
        name="cuestionarios"
    ),
    path("clases/<int:clase_id>/cuestionarios/nuevo/",views_profesor.profesor_cuestionario_crear, name="cuestionario_crear"),
    path(
    "profesor/cuestionarios/<int:cuestionario_id>/editar/",
    views_profesor.profesor_cuestionario_editar,
    name="profesor_cuestionario_editar"
),

    # ===== PREGUNTAS =====
    path(
        "cuestionarios/<int:cuestionario_id>/preguntas/",
        views_profesor.profesor_preguntas,
        name="preguntas"
    ),
    path(
    "pregunta/nueva/<int:cuestionario_id>/",
    views_profesor.profesor_pregunta_form,
    name="pregunta_crear"
),

path(
    "pregunta/editar/<int:cuestionario_id>/<int:pregunta_id>/",
    views_profesor.profesor_pregunta_form,
    name="pregunta_editar"
),

]
