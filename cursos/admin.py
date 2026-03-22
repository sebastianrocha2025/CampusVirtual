from django.contrib import admin
from .models import Curso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)



admin.site.site_header = "Administración del Campus Virtual"
admin.site.site_title = "Campus Virtual"
admin.site.index_title = "Panel del Director"