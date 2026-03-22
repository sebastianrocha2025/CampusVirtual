from django.contrib import admin
from django import forms
from .models import (
    Cuestionario,
    Pregunta,
    Opcion,
    EntregaCuestionario,
    RespuestaOpcion,
    Clase

)
from .models import MaterialClase


admin.site.register(MaterialClase)

class MaterialClaseInline(admin.TabularInline):
    model = MaterialClase
    extra = 1

# -------------------------
# FORM FILTRADO
# -------------------------
class RespuestaOpcionForm(forms.ModelForm):
    class Meta:
        model = RespuestaOpcion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.entrega_id:
            cuestionario = self.instance.entrega.cuestionario
            self.fields["opcion"].queryset = Opcion.objects.filter(
                pregunta__cuestionario=cuestionario
            )
        else:
            self.fields["opcion"].queryset = Opcion.objects.none()


# -------------------------
# INLINES
# -------------------------
class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 2


class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1
    show_change_link = True


class RespuestaOpcionInline(admin.TabularInline):
    model = RespuestaOpcion
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "opcion":
            try:
                entrega_id = request.resolver_match.kwargs.get("object_id")
                if entrega_id:
                    entrega = EntregaCuestionario.objects.get(pk=entrega_id)
                    kwargs["queryset"] = Opcion.objects.filter(
                        pregunta__cuestionario=entrega.cuestionario
                    )
                else:
                    kwargs["queryset"] = Opcion.objects.none()
            except EntregaCuestionario.DoesNotExist:
                kwargs["queryset"] = Opcion.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ("titulo", "curso", "orden", "visible")
    list_filter = ("curso", "visible")
    inlines = [MaterialClaseInline]
    
# -------------------------
# ADMINS
# -------------------------
@admin.register(Cuestionario)
class CuestionarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'clase', 'activo')
    list_filter = ('activo', 'clase')
    search_fields = ('titulo',)
    inlines = [PreguntaInline]


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'cuestionario')
    list_filter = ('cuestionario',)
    search_fields = ('texto',)
    inlines = [OpcionInline]


@admin.register(EntregaCuestionario)
class EntregaCuestionarioAdmin(admin.ModelAdmin):
    list_display = ('cuestionario', 'inscripcion')
    list_filter = ('cuestionario',)
    inlines = [RespuestaOpcionInline]


@admin.register(RespuestaOpcion)
class RespuestaOpcionAdmin(admin.ModelAdmin):
    list_display = ('entrega', 'opcion')
