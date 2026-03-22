from django.contrib import admin
from django.urls import path, include
from core.views import home
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # HOME PÚBLICO
    path('', home, name='home'),
    path('core/', include('core.urls')),

    # AUTENTICACIÓN
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # CAMPUS
    path('cursos/', include('cursos.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path('academico/', include('academico.urls')),
    path('profesor/', include('academico.urls_profesor')),

    # ADMIN
    path('admin/', admin.site.urls),
]

# ✅ SOLO en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)