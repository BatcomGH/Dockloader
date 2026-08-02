# Archivo: api/urls.py
from django.urls import path
from . import views # Importamos el archivo views.py de esta misma carpeta

urlpatterns = [
    # path('ruta-en-la-url/', la_funcion_de_tu_vista, nombre_de_referencia)
    path('descargar_video/', views.descargar_video_api, name='descargar_video'),
    path('descargar_musica/', views.descargar_musica_api, name='descargar_musica'),
    path('descargar_audio/', views.descargar_audio_api, name='descargar_audio'),
]