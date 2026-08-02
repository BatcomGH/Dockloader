import os
import json
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import downloader
from . import video2music

@csrf_exempt 
def descargar_video_api(request):
    if request.method == 'POST':
        try:
            print("¡Recibiendo petición POST para descargar!")
            
            data = json.loads(request.body)
            video_url = data.get('url')
            
            if not video_url:
                response = JsonResponse({'error': 'URL no proporcionada'}, status=400)
                response['Access-Control-Allow-Origin'] = '*'
                return response
            
            dirDescargas = "/tmp"
            ruta_archivo_descargado = downloader.descargar_video(video_url, dirDescargas)

            if not ruta_archivo_descargado:
                response = JsonResponse({'error': 'Error al descargar el video'}, status=500)
                response['Access-Control-Allow-Origin'] = '*'
                return response

            print(f"Video listo en: {ruta_archivo_descargado}. Enviando a Angular...")

            archivo = open(ruta_archivo_descargado, 'rb')
            nombre_archivo = os.path.basename(ruta_archivo_descargado)
            
            response = FileResponse(archivo, as_attachment=True, filename=nombre_archivo)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response

        except Exception as e:
            print(f"(!) Error interno: {str(e)}")
            if 'is not a valid URL' in str(e):
                error_response = JsonResponse({'error': f'\"{video_url}\" es una URL no válida'}, status=400)
            elif 'This video may be inappropriate for some users.' in str(e):
                error_response = JsonResponse({'error': f'El video de la URL \"{video_url}\" tiene restricción de edad y no puede ser descargado. Configurar cookies de sesión para descargar videos restringidos.'}, status=403)
            else:
                error_response = JsonResponse({'error': f'Error al intentar descargar el video: {str(e)}'}, status=500)
            error_response['Access-Control-Allow-Origin'] = '*'
            return error_response

    response = JsonResponse({'mensaje': 'Método no permitido'}, status=405)
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt 
def descargar_audio_api(request):
    if request.method == 'POST':
        try:
            print("¡Recibiendo petición POST para descargar!")
            
            data = json.loads(request.body)
            video_url = data.get('url')
            
            if not video_url:
                # SOLUCIÓN 1: Agregar CORS a este error
                response = JsonResponse({'error': 'URL no proporcionada'}, status=400)
                response['Access-Control-Allow-Origin'] = '*'
                return response
        
            ruta_archivo_descargado = video2music.audDownMain(video_url)

            if ruta_archivo_descargado == "NoTitle":
                raise Exception("No se pudo obtener el título del video debido a un error. Posiblemente un error 429 (Muchas solicitudes). Espere algunos minutos antes de intentar nuevamente.")

            if not ruta_archivo_descargado:
                # SOLUCIÓN 1: Agregar CORS a este error
                response = JsonResponse({'error': 'Error al descargar el video'}, status=500)
                response['Access-Control-Allow-Origin'] = '*'
                return response

            print(f"Video listo en: {ruta_archivo_descargado}. Enviando a Angular...")

            archivo = open(ruta_archivo_descargado, 'rb')
            nombre_archivo = os.path.basename(ruta_archivo_descargado)
            
            response = FileResponse(archivo, as_attachment=True, filename=nombre_archivo)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response

        except Exception as e:
            print(f"(!) Error interno: {str(e)}")
            if 'is not a valid URL' in str(e):
                error_response = JsonResponse({'error': f'\"{video_url}\" es una URL no válida'}, status=400)
            elif 'This video may be inappropriate for some users.' in str(e):
                error_response = JsonResponse({'error': f'El video de la URL \"{video_url}\" tiene restricción de edad y no puede ser descargado. Configurar cookies de sesión para descargar videos restringidos.'}, status=403)
            else:
                error_response = JsonResponse({'error': f'Error al intentar descargar el video: {str(e)}'}, status=500)
            error_response['Access-Control-Allow-Origin'] = '*'
            return error_response

    response = JsonResponse({'mensaje': 'Método no permitido'}, status=405)
    response['Access-Control-Allow-Origin'] = '*'
    return response