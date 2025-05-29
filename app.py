from flask import Flask, render_template, request, redirect, url_for,send_file,after_this_request
import yt_dlp
from datetime import timedelta
import os
from bs4 import BeautifulSoup
import threading
import time
import requests
import instaloader
import re
from moviepy.editor import VideoFileClip

app = Flask(__name__)



def login_ig():
    USERNAME = 'myrabella.contact@gmail.com'
    PASSWORD = 'VIDA@2018'
    
    L = instaloader.Instaloader()
    
    
    return L

L = login_ig()

def shortcode_extract(url):
    match = re.search(r'/reel/([^/]+)/', url)
    if not match:
        print("URL inválida! Certifique-se de que é um link de Reels.")
        exit()

    shortcode = match.group(1)
    return shortcode



def delete_file_later(filepath,ext, delay=20):
    def delayed_delete():
        time.sleep(delay)
        if ext == 'mp3':
            try:
                os.remove(filepath)
                print(f"Arquivo {filepath} apagado com sucesso.")
            except Exception as e:
                print(f"Erro ao apagar arquivo: {e}")
                
            file = filepath.replace('mp3','mp4')
            print(file)
            try:
                os.remove(file)
            except Exception as e:
                print(e)
            
        else:
            try:
                os.remove(filepath)
                print(f"Arquivo {filepath} apagado com sucesso.")
            except Exception as e:
                print(f"Erro ao apagar arquivo: {e}")
            
    threading.Thread(target=delayed_delete).start()

@app.route('/home')  
def home():

    return render_template('index.html')

@app.route('/')
def index_redirect():
    
        return redirect(url_for('home'))

@app.route('/sobre') 
def sobre():
    return render_template("yt_dw.html")


@app.route('/termos') 
def termos():
    return render_template("termos.html")

@app.route('/privacidade') 
def privacidade():
    return render_template("privacy.html")


def get_instagram_reel_info(reel_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    response = requests.get(reel_url, headers=headers)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Título (muitas vezes vem como descrição)
    title_tag = soup.find("meta", property="og:title")
    title = title_tag['content'] if title_tag else "Sem título"
    
    thumbnail_tag = soup.find("meta", property="og:image")
    thumbnail = thumbnail_tag['content'] if thumbnail_tag else None

    
    shortcode = shortcode_extract(reel_url)

    post = instaloader.Post.from_shortcode(L.context, shortcode)
    
    # DADOS
    duration = post.video_duration  # em segundos
    author = post.owner_username

    
    
    return title,author,thumbnail,duration
        



def get_video_info_from_youtube(video_url):
    print("chegou aqui no youtube")
    if "youtube.com" in video_url or "youtu.be" in video_url:
        video_id = extract_video_id_py(video_url)
        
        ydl_opts = {
            'cookies': 'youtube.com_cookies.txt',
            'quiet': True,  
            'skip_download': True,
        }   
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        titulo = info.get('title')
        canal = info.get('uploader')
        duracao_video = str(timedelta(seconds=info.get('duration')))
        return {
            'title': f'{titulo}',
            'thumbnail_url': f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg',
            'uploader': f'{canal}',
            'duration': f'{duracao_video}',
            'formats': [
                {'itag': '22', 'label': 'Mp4 720p', 'ext': 'mp4', 'download_url': '#simulated_download_link_720p'},
                {'itag': '18', 'label': 'Mp4 360p', 'ext': 'mp4', 'download_url': '#simulated_download_link_360p'},
                {'itag': '140', 'label': 'Mp3 Áudio (128kbps)', 'ext': 'mp3', 'download_url': '#simulated_download_link_audio_m4a'},
            ],
            'original_url': video_url,
            'error': None
        }
    return {'error': 'Link inválido ou não suportado.', 'title': None}

def get_video_info_from_instagram(video_url):
    
    print('pelo menos chegou aqui')
    if "instagram.com" in video_url:
        
        
        titulo,canal,thumbnail_url,duracao = get_instagram_reel_info(video_url)
        
        print(canal)
        duracao_video = duracao
        #duracao_video = str(timedelta(duracao))
        return {
            'title': f'{titulo}',
            'thumbnail_url': f'{thumbnail_url}',
            'uploader': f'{canal}',
            'duration': f'{duracao_video}',
            'formats': [
                {'itag': '22', 'label': 'Mp4 720p', 'ext': 'mp4', 'download_url': '#simulated_download_link_720p'},
                {'itag': '140', 'label': 'Mp3 Áudio (128kbps)', 'ext': 'mp3', 'download_url': '#simulated_download_link_audio_m4a'},
            ],
            'original_url': video_url,
            'error': None
        }
    return {'error': 'Link inválido ou não suportado.', 'title': None}


def extract_video_id_py(url):
    video_id = ''
    if "youtube.com/watch?v=" in url:
        video_id = url.split('v=')[1].split('&')[0]
    elif "youtu.be/" in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
    return video_id or 'dQw4w9WgXcQ' # Fallback

# Em produção, o processamento do link deveria ser POST.
@app.route('/youtube-downloader', methods=['GET', 'POST'])
def youtube_downloader_page():
    video_info = None
    error_message = None
    submitted_url = ''

    if request.method == 'POST':
        video_url = request.form.get('video-url')
        submitted_url = video_url 
        if video_url:
            
            video_data = get_video_info_from_youtube(video_url)
            if video_data and not video_data.get('error'):
                video_info = video_data
            else:
                error_message = video_data.get('error', 'Ocorreu um erro ao processar o link.')
        else:
            error_message = "Por favor, insira um link do YouTube."

    return render_template('yt_dl.html',
                           video_info=video_info,
                           error_message=error_message,
                           submitted_url=submitted_url)

@app.route('/instagram_reels_downloader_page', methods=['GET', 'POST'])
def instagram_reels_downloader_page():
    video_info = None
    error_message = None
    submitted_url = ''

    if request.method == 'POST':
        video_url = request.form.get('video-url')
        submitted_url = video_url 
        if video_url:
            
            video_data = get_video_info_from_instagram(video_url)
            if video_data and not video_data.get('error'):
                video_info = video_data
            else:
                error_message = video_data.get('error', 'Ocorreu um erro ao processar o link.')
        else:
            error_message = "Por favor, insira um link de reels."

    return render_template('ig_dl.html',
                           video_info=video_info,
                           error_message=error_message,
                           submitted_url=submitted_url)


@app.route('/download_ig_video')
def download_ig_video():
    itag = request.args.get('itag')
    video_url = request.args.get('url')
    if not video_url or not itag:
        return "Erro: URL do vídeo ou formato não especificado.", 400
    
    
    
    shortcode = shortcode_extract(video_url)
    filename = (f'{shortcode}.mp4')
    L = instaloader.Instaloader(
    download_video_thumbnails=False,
    download_geotags=False, 
    download_comments=False,
    save_metadata=False,
    post_metadata_txt_pattern='',
    dirname_pattern='.',
    filename_pattern=shortcode
)
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    
    match itag:
    
        case '22':
            print('720p')
            ext = 'mp4'
            

        case '140':
            print('mp3')
            ext = 'mp3'
            
    if post.is_video:
        L.download_post(post, target='.')
    
    
    print(filename)
    if ext == 'mp3' :
        clip = VideoFileClip(filename)
        clip.audio.write_audiofile(f'{shortcode}.mp3')
        clip.close()
        time.sleep(2)
        #os.remove(filename)
        filename = f'{shortcode}.mp3'
    
    
    delete_file_later(filename,ext, delay=20)
    return send_file(filename, as_attachment=True, conditional=True)


@app.route('/download_yt_video')
def download_yt_video():
    
    video_url_to_download = request.args.get('url')
    itag = request.args.get('itag')
    filename = request.args.get('filename', 'video.mp4')

    if not video_url_to_download or not itag:
        return "Erro: URL do vídeo ou formato não especificado.", 400
    
    match itag:
    
        case '22':
            print('720p')
            ext = 'mp4'
            ydl_opts = {
                'format': 'bestvideo[height<=720][ext=mp4]+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': False,
            }
            
        case '18':
            print('360p')
            ext = 'mp4'
            ydl_opts = {
                'format': 'bestvideo[height<=360][ext=mp4]+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': False,
            }

        case '140':
            print('mp3')
            ext = 'mp3'
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s' 
            }
            
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        
        info = ydl.extract_info(video_url_to_download,download=False)
        print(ydl.prepare_filename(info))
        filename = info.get('title')
        filename = ydl.prepare_filename(info)
        video = ydl.download([video_url_to_download])
    
    print(filename)
    if ext == 'mp3' :
        filename = filename.replace('.mp4', '.mp3')
        filename = filename.replace('.webm', '.mp3')
    
    delete_file_later(filename,ext, delay=20)
    return send_file(filename, as_attachment=True, conditional=True)

@app.route('/tk_downloader_page')
def tk_downloader_page():
    
    
    
    return render_template('tk_dl.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # usa a porta definida pelo Railway
    app.run(host='0.0.0.0', port=port, debug=True)

                                     
