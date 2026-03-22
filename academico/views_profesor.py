from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .models import Clase, Cuestionario, Pregunta, Opcion, MaterialClase
from .forms import ClaseForm, CuestionarioForm,  PreguntaForm, OpcionFormSet
from cursos.models import Curso
@staff_member_required
def profesor_clases(request):
    clases = Clase.objects.select_related("curso")
    return render(request, "profesor/clases/lista.html", {
        "clases": clases
    })




@staff_member_required
def profesor_clase_editar(request, clase_id):

    clase = get_object_or_404(Clase, id=clase_id)
    curso = clase.curso

    if request.method == "POST":
        form = ClaseForm(request.POST, instance=clase)

        if form.is_valid():
            form.save()

            return redirect(
                "profesor:profesor_clases_por_curso",
                curso.id
            )

    else:
        form = ClaseForm(instance=clase)

    return render(request, "profesor/clases/form.html", {
        "form": form,
        "clase": clase,
        "curso": curso
    })

@staff_member_required
def profesor_clases_por_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    clases = Clase.objects.filter(curso=curso)

    return render(request, "profesor/clases/por_curso.html", {
        "curso": curso,
        "clases": clases
    })
# -------------------------
# CREAR CLASE
# -------------------------
@staff_member_required
def profesor_clase_crear(request, curso_id):

    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == "POST":

        form = ClaseForm(request.POST, request.FILES)

        if form.is_valid():

            clase = form.save(commit=False)
            clase.curso = curso
            clase.save()

            # subir archivo si existe
            archivo = request.FILES.get("archivo")

            if archivo:
                MaterialClase.objects.create(
                    clase=clase,
                    titulo="Material de clase",
                    archivo=archivo
                )

            return redirect(
                "profesor:profesor_clases_por_curso",
                curso.id
            )

    else:
        form = ClaseForm(initial={"curso": curso})

    return render(request, "profesor/clases/form.html", {
        "form": form,
        "curso": curso
    })




@staff_member_required
def profesor_cuestionarios(request, clase_id):
    clase = Clase.objects.get(id=clase_id)
    cuestionarios = Cuestionario.objects.filter(clase=clase)
    return render(request, "profesor/cuestionarios/lista.html", {
        "clase": clase,
        "cuestionarios": cuestionarios
    })

@staff_member_required
def profesor_cuestionario_crear(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)

    if request.method == "POST":
        form = CuestionarioForm(request.POST)
        if form.is_valid():
            cuestionario = form.save(commit=False)
            cuestionario.clase = clase
            cuestionario.save()
            return redirect("profesor:cuestionarios", clase.id)
    else:
        form = CuestionarioForm()

    return render(request, "profesor/cuestionarios/form.html", {
        "form": form,
        "clase": clase
    })

@staff_member_required
def profesor_cuestionario_editar(request, cuestionario_id):
    cuestionario = get_object_or_404(Cuestionario, id=cuestionario_id)

    if request.method == "POST":
        form = CuestionarioForm(request.POST, instance=cuestionario)
        if form.is_valid():
            form.save()
            return redirect("profesor:cuestionarios", cuestionario.clase.id)
    else:
        form = CuestionarioForm(instance=cuestionario)

    return render(request, "profesor/cuestionarios/form.html", {
        "form": form,
        "clase": cuestionario.clase
    })

@staff_member_required
def profesor_preguntas(request, cuestionario_id):
    cuestionario = Cuestionario.objects.get(id=cuestionario_id)
    preguntas = cuestionario.preguntas.all()
    return render(request, "profesor/preguntas/lista.html", {
        "cuestionario": cuestionario,
        "preguntas": preguntas
    })


@staff_member_required
def profesor_pregunta_form(request, cuestionario_id, pregunta_id=None):

    cuestionario = get_object_or_404(Cuestionario, id=cuestionario_id)

    if pregunta_id:
        pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    else:
        pregunta = None

    if request.method == "POST":

        form = PreguntaForm(request.POST, instance=pregunta)

        if pregunta:
            formset = OpcionFormSet(
                request.POST,
                request.FILES,
                instance=pregunta
            )
        else:
            formset = OpcionFormSet(
                request.POST,
                request.FILES
            )

        if form.is_valid() and formset.is_valid():

            # 🔥 validar UNA sola correcta
            correctas = sum(
                1 for f in formset.cleaned_data
                if f and f.get("es_correcta") and not f.get("DELETE", False)
            )

            if correctas != 1:
                return render(request, "profesor/preguntas/form.html", {
                    "form": form,
                    "formset": formset,
                    "cuestionario": cuestionario,
                    "error": "Debe haber exactamente UNA opción correcta."
                })

            pregunta = form.save(commit=False)
            pregunta.cuestionario = cuestionario
            pregunta.save()

            formset.instance = pregunta
            formset.save()

            return redirect("profesor:preguntas", cuestionario.id)

    else:
        form = PreguntaForm(instance=pregunta)

        if pregunta:
            formset = OpcionFormSet(instance=pregunta)
        else:
            formset = OpcionFormSet()

    return render(request, "profesor/preguntas/form.html", {
        "form": form,
        "formset": formset,
        "cuestionario": cuestionario
    })