import instaloader
import re

def login_ig():
    USERNAME = 'myrabella.contact@gmail.com'
    PASSWORD = 'VIDA@2018'
    L = instaloader.Instaloader()
    
    return L


def shortcode_extract(url):
    match = re.search(r'/reel/([^/]+)/', url)
    if not match:
        print("URL inválida! Certifique-se de que é um link de Reels.")
        exit()

    shortcode = match.group(1)
    return shortcode
    
    
url = 'https://www.instagram.com/reel/DH3z1_jyoHU/?utm_source=ig_web_copy_link'


shortcode = shortcode_extract(url)
L = login_ig()


# ======== CONFIGURAÇÃO DO INSTALOADER ========
L = instaloader.Instaloader(
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    post_metadata_txt_pattern='',
    dirname_pattern='.',
    filename_pattern=shortcode
)

# ======== LOGIN ========


# ======== DOWNLOAD E INFORMAÇÕES ========
try:
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    
    # DADOS
    duration = post.video_duration  # em segundos
    author = post.owner_username
    
    print()
    
    print(f"🎬 Autor: {author}")
    print(f"⏱️ Duração: {duration:.2f} segundos")
    
    if post.is_video:
        L.download_post(post, target='.')
        print(f"✅ Vídeo salvo como: {shortcode}.mp4")
    else:
        print("❌ Esse post não é um vídeo.")

except Exception as e:
    print(f"❌ Erro ao baixar o Reels: {e}")