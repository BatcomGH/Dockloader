import os
import yt_dlp
from . import cookies

def descargar_video(url, output_path="/app/downloads"):
    opciones = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  
            'merge_output_format': 'mp4',
            'js_runtimes': {'deno': {}},
            'restrictfilenames': True,
            'noplaylist': True,
        }

    if not cookies.isCookiesEmpty():
        opciones['cookiefile'] = cookies.rutaCookies

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            
            if 'requested_downloads' in info_dict:
                final_path = info_dict['requested_downloads'][0]['filepath']
            else:
                final_path = ydl.prepare_filename(info_dict)
                if not final_path.endswith('.mp4'):
                    base_path, _ = os.path.splitext(final_path)
                    final_path = f"{base_path}.mp4"
        
        if not os.path.exists(final_path):
            raise Exception(f"Error en el servidor: el archivo final no se encuentra en la ruta esperada: {final_path}")

        return final_path 
        
    except Exception as e:
        print("!"*100)
        print(f"Error en yt-dlp: {str(e)}") 
        raise e