import os
import yt_dlp
from . import cookies

def descargar_video(url, output_path="/app/downloads"):

    if not cookies.isCookiesEmpty():
        opciones = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  
            'merge_output_format': 'mp4',
            #'js_runtimes': {'node': {}},
            'cookiefile': cookies.rutaCookies,
            'restrictfilenames': True,
        }
    else:
        opciones = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            #'js_runtimes': {'node': {}},
            'restrictfilenames': True,
        }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)

        base_path, _ = os.path.splitext(file_path)
        final_path = f"{base_path}.mp4"

        if not os.path.exists(final_path):
            final_path = file_path

        return final_path 
        
    except Exception as e:
        print("!"*100)
        print(f"Error en yt-dlp: {str(e)}") 
        raise e