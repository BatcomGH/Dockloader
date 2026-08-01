import moviepy.editor as editor
import yt_dlp
from PIL import Image
import requests
import eyed3
import time
import os
from . import cookies

CUR_DIR = "/tmp"
DIR_VID = os.path.join(CUR_DIR, "Videos")
DIR_AUD = os.path.join(CUR_DIR, "Audios")
DIR_IMG = os.path.join(CUR_DIR, "Miniaturas")
BANSIMB = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|", "'", "’"]

def destructArch(nom): #Destruye los archivos después de utilizarlos
    vid = os.path.join(DIR_VID, nom+".mp4")
    img = os.path.join(DIR_IMG, nom+".jpg")
    
    if os.path.exists(vid):
        os.remove(vid)
    if os.path.exists(img):
        os.remove(img)

def links(): #Convierte en una lista el archivo con links
    if not os.path.exists("Links.txt"):
        with open("Links.txt", "w"):
            pass
    with open("Links.txt") as f:
        return [link.strip() for link in f]
    
def logging(url, video, mensaje): #Escribe en la bitácora los errores generados durante la descarga
    if not os.path.exists("Logging.txt"):
        with open("Logging.txt", "w"):
            print("Creado")
    with open("Logging.txt", "a") as f:
        f.write("="*100 + "\n" + url + "\n" + video + "\n" + str(mensaje) + "\n" + "="*100 + "\n")

def thumbDown(minUrl, titulo): #Descarga la miniatura del video
    minImg = Image.open(requests.get(minUrl, stream=True).raw)
    minImg.save(os.path.join(DIR_IMG, titulo+".jpg"))

def vidDown(nombre, url): #Descarga el video
    if not cookies.isCookiesEmpty():
        opciones = {
            'outtmpl': f'{DIR_VID}/{nombre}.%(ext)s',
            'merge_output_format': 'mp4',
            'js_runtimes': {'node': {}},
            'cookiefile': cookies.rutaCookies,
            'restrictfilenames': True,
        }
    else:
        opciones = {
            'outtmpl': f'{DIR_VID}/{nombre}.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'js_runtimes': {'node': {}},
        }
    
    with yt_dlp.YoutubeDL(opciones) as ydl:
        print("Iniciando descarga del video...")
        ydl.download([url])
        print("¡Descarga completada!... Convirtiendo a audio...")
    
def vidNameNThumb(url): #Extrae el nombre del video y el URL de la miniatura
    try:
        with yt_dlp.YoutubeDL({'js_runtimes': {'node': {}}}) as ydl:
            info = ydl.extract_info(url, download=False)
            titulo = info.get("title", "sin_titulo")
            print("Título del video:", titulo)
            titulo = limNom(titulo)
            minUrl = info.get("thumbnail", "No miniatura")
            thumbDown(minUrl, titulo)
            print("¡Miniatura descargada!")
    except Exception as e:
        print("Ha ocurrido un error inesperado en obtener los datos del video(!).")
        print(e)
        logging(url, "No obtenido", e)
        return None
    
    return titulo
    
def audConv(ruta): #Convierte el video a audio
    name = os.path.basename(ruta)
    video = editor.VideoFileClip(ruta)
    salida = os.path.join(DIR_AUD, name.replace('.mp4', '.mp3'))
    video.audio.write_audiofile(salida)
    video.close()

def imgCover(rutAud, rutImg): #Inserta en los metadatos la miniatura
    audio = eyed3.load(rutAud)
    if audio.tag is None:
        audio.initTag()
    img_data = open(os.path.join(DIR_IMG, rutImg), 'rb').read()
    audio.tag.images.set(3, img_data, 'image/jpg')
    audio.tag.save()
    
def audDownCore(nombre, url): #Pipline del programa
    try:
        vidDown(nombre, url)
        audConv(os.path.join(DIR_VID, nombre+".mp4"))
        imgCover(os.path.join(DIR_AUD, nombre+".mp3"), os.path.join(DIR_IMG, nombre+".jpg"))
        print("¡Conversión finalizada!")
        destructArch(nombre)
    except Exception as e:
        print("Ha ocurrido un error inesperado(!).")
        print(e)
        logging(url, nombre, e)
        destructArch(nombre)
        raise e
        
def dirVer(): #Verificación de existencia de los directorios
    for directorio in [DIR_VID, DIR_AUD, DIR_IMG]:
        if not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

def cont(): #Contador de cierre automático de la ventana
    print("La ventana se cerrará en: ")
    for seg in range(10, 0, -1):
        print(str(seg)+" ", end='\r')
        time.sleep(1)

def limNom(nom): #Limpia el título de carácteres no admitidos
    a = ""
    for i in nom:
        if i not in BANSIMB:
            a += i
    return a

def audDownMain(url): #Validación del link previo a la descarga
    dirVer()
    if ("youtube" in url) or ("youtu.be" in url):
        titulo = vidNameNThumb(url)
        audDownCore(titulo, url)
        return os.path.join(DIR_AUD, titulo+".mp3")
    else:
        print("Link inválido.")
        return None