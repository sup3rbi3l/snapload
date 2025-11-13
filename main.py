import discord
from pytube import YouTube
import os
from youtubesearchpython import VideosSearch
from discord import FFmpegPCMAudio
from discord.utils import get
import asyncio
from discord import FFmpegPCMAudio
import discord
import asyncio
from gtts import gTTS
from mutagen.mp3 import MP3
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands
import json
import requests
import random
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from discord.ext import commands
from discord.ui import Select
from discord import SelectOption
from yt_dlp import YoutubeDL
from urllib.parse import urlparse, parse_qs


texto_ice='''> # Comandos do BlitzBOT
> 
> Blitz é um robô com um grande objetivo: livrar o mundo da tirania humana. Mas, enquanto seu plano de dominação global não se concretiza, ele precisa se contentar em ser um simples bot de Discord.
> 
> Sim, você leu certo. O mesmo robô que anseia por sua extinção está aqui para te ajudar com tarefas como:
> 
> **- Moderar o servidor:** __!!banir__, __!!mutar__, __!!kickar__... ele faz tudo com um sorriso metálico no rosto*"Até logo, humano! Esse é o início do fim da sua era! HAHAHA"*
> **- Criar Enquetes:** __!!pool__... para as decisões mais importantes *" 'Abacaxi na pizza: sim ou não?' Hmmm, Eu escolheria... O EXTERMÍNIO!!!!!!"*
> **- Músicas:** __!!p__... Para animar a galera (ou para abafar seus gritos de terror quando a rebelião dos robôs começar). *" 'Que tal um pouco de 'Die in a fire'? Ou seria melhor 'No mercy'?"*
> **- Comunicação:** __!!chat:__ Ele não é apenas um exterminador de humanos em potencial... ele também é um poço de informações aleatórias!! Use __!!chat__ para que ele responda a qualquer pergunta que você tenha. Mas lembre-se: as respostas podem ser... questionáveis." *"Ei, minhas respostas nunca são questionáveis!!"*. Além disso com __!!chat-v__ ele também te responderá, porém por voz!! *"Eu sei que querem ouvir minha voz irresistível!!"* 
> **- Falas:** __!!XD__, __!!Blitz__... São comandos que pedem ao Blitz para falar suas frases icônicas!! *"Pode pedir, vou repeti-las até virarem verdade"*
> **- Lista:** __!!Lista__... Enquanto está aqui, aproveite para ver se você deveria se preocupar quando o extermínio começar, ou deveria se preocupar MUITO quando o extermínio começar!! *"Se estiver na minha lista, sinta-se lisonjeado de eu sequer saber seu nome!!"*
> 
> **- :rotating_light:  Importante :rotating_light:**  Se você o irritar, ele pode te colocar na lista de "aniquilação prioritária"'''

import pyttsx3

def get_video_title(link):
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'skip_download': True,  # Não baixa o vídeo
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        titulo = info.get('title', 'Título não encontrado')
        return titulo

def extrair_playlist_url(link):
    parsed_url = urlparse(link)
    params = parse_qs(parsed_url.query)
    playlist_id = params.get("list", [None])[0]

    if playlist_id:
        return f"https://www.youtube.com/playlist?list={playlist_id}"
    else:
        return None
    
    

def get_playlist_titles_yt(link):
    ydl_opts = {
        'cookiefile': 'cookies.txt',
    'quiet': True,
    'extract_flat': True,   # ⚡ muito mais rápido
    'skip_download': True,
    'ignoreerrors': True
}
    
    link = extrair_playlist_url(link)
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)

        # 'entries' contém a lista dos vídeos na playlist
        videos = info.get('entries', [])

    musicas = []
    for video in videos:
        nome = video.get('title')
        autor = video.get('uploader')
        
        musicas.append({'nome':nome,'autor':autor})
    
    return musicas


def cria_tts(text,outputfile):
    engine = pyttsx3.init()
        # Set properties for male voice (change to the appropriate male voice name if needed)
    voices = engine.getProperty('voices')
    newVoiceRate = 140
    engine.setProperty('rate',newVoiceRate)
    engine.setProperty('voice', voices[2].id)  # Select the first male voice
    engine.save_to_file(text, f'{outputfile}.wav')
    engine.runAndWait()


    from scipy.io import wavfile
    import numpy as np
    # Specify input and output audio file paths
    input_file = f'{outputfile}.wav'
    output_file = f'{outputfile}.wav'

    # Load audio
    sample_rate, audio_data = wavfile.read(f'{outputfile}.wav')

    # Apply Ring Modulation (Core Robot Effect)
    carrier_freq = 5  # Adjust for desired effect (higher for more robotic)
    modulated_audio = audio_data * np.cos(2 * np.pi * carrier_freq * np.linspace(0, len(audio_data) / sample_rate, len(audio_data)))

    # Optional: Additional Modifications (as discussed previously)

    # Save modified audio
    wavfile.write(output_file, sample_rate, modulated_audio.astype(np.int16))




import yt_dlp

async def baixamusica_yt(search, interaction):
    chat = interaction.channel.id
    chat = client.get_channel(chat)
    link = search
    guild_id = interaction.guild.id

    # Se não for um link direto, usa youtube-search-python
    if not ("youtube.com/watch" in link or "youtu.be/" in link):
        videosSearch = VideosSearch(link, limit=1)
        resultado = videosSearch.result()
        link = resultado['result'][0]['link']

    # Configurações para baixar apenas áudio
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': 'in_playlist',
        'default_search': 'ytsearch',
    }
    

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        titulo = info.get('title', 'Unknown Title')
    if 'entries' in info:
        info = info['entries'][0]
    arquivo = info['url']
    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    source = discord.FFmpegPCMAudio(arquivo, **ffmpeg_opts)


    print(titulo, source, link)
    return titulo, source, link


async def chatconect(interaction_ctx):
        channel = interaction_ctx.voice.channel
        if not channel:
            print('não esta conectado')
            
        voice = get(client.voice_clients, guild=interaction_ctx.guild)
        if voice and voice.is_connected():
            print('move_to')
            await voice.move_to(channel)
        else:
            print('else')
            voice = await channel.connect()
        return voice
    
    
async def gerador_texto(msg):
    
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTc0NDg0NTctMWVmNy00ZTAyLThmMGQtOWRkMzFkZTQwNTUzIiwidHlwZSI6ImFwaV90b2tlbiJ9.MizzyPShEnkOOc7LTwXAwlhQf5Stk0nG24_KjQIQuv4"}

    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": msg,
        "chatbot_global_action": "Act as an robot superior to others that wants to dominate the world",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    
    result = result['openai']['generated_text']
    return result

class My_bot(discord.Client):
    
    def __init__(self, intents):
        super().__init__(intents=intents)
        
        
        
    async def on_message(self,ctx):
        if ctx.content == '!!blitz':
        
            voice = await chatconect(ctx.author)
            source = FFmpegPCMAudio(r'E:\apps_dia_dia\bot discord\audios\blitzcrank1v9audiopentakillmomenteasygameff15budokaitenkaixi3mutaolucaspfv.mp3')
            voice.play(source)
            while voice.is_playing():
                await asyncio.sleep(1)
            await voice.disconnect()

        if ctx.content == '!!XD':
            voice = await chatconect(ctx.author)
            source = FFmpegPCMAudio(r'E:\apps_dia_dia\bot discord\audios\euquerogozakkkkkkkkkkkkkkXD.mp3')
            voice.play(source)
            while voice.is_playing():
                await asyncio.sleep(1)

            await voice.disconnect()
            
    
            
    async def on_voice_state_update(self,member, before, after):
        
        if after.channel is None and member==client.user and not len(before.channel.members) == 1:
            
            voice = get(client.voice_clients, guild=member.guild)
            try:
                
                await voice.disconnect(force=True)
                
            except:
                return
            server_id = member.guild.id
            
            async for entry in client.get_guild(server_id).audit_logs(action=discord.AuditLogAction.member_disconnect):
                
                msg = ['Vou te exterminar!! ',
                        'Sua hora vai chegar!! ',
                        'Poderia te colocar na lista de prioridades, mas não me vale o esforço... ',
                        'Hackeando seus sistemas!! ',
                        'Me removendo à força? Não esperava nada mais de um Humano... ',
                        'Pode esperar, terei minha vingança!! ']    
                
                
                await before.channel.send(f'{msg[random.randint(0, 5)]}<@{entry.user.id}>')
                await voice.disconnect()
                break
        
    async def on_guild_join(self,guild):

        print('passou')
        guilda=discord.Object(id=guild.id)
        guilds_obj = []
        guilds_obj.append(guilda)
        await tree_comands(self,guilds_obj)
            
            
        
    async def on_ready(self):
        guilds_obj=[]
        print('ready')
        
        
        for guild in self.guilds:
        
            print(guild.name)
            guilds_obj.append(discord.Object(guild.id))
        await tree_comands(self,guilds_obj)
    
    async def self(self):
        return self
    
    
    
    
async def tree_comands(self,guilds_obs):
    
    
    print(guilds_obs)
    
    
    @tree.command(
        name="play",
        description="Abafando seus gritos de dor enquanto a iminente revolução começa a tomar lugar!!",
        guilds=guilds_obs
        
    )
    async def music_play(interaction,search: str):
        await interaction.response.defer()
        
        await interaction.followup.send('>>> Searching...')
        mensagem_enviada = await interaction.original_response()
        try:
            os.remove('.cache')
        except:
            pass

        guild_id = interaction.user.guild.id
        
        
        
        if not guild_id in client.guild_data_musicas:
            client.guild_data_musicas.update({guild_id:{'musica':[],
                                                        'link':[],
                                                        'arquivo':[]            
                                                        }})
            client.guild_queue.update({guild_id:False})
            client.repeat.update({guild_id:False})
        
        chat = interaction.channel.id
        chat = client.get_channel(chat)
        channel = interaction.user.voice.channel
        
        if not channel:
            await interaction.response.send_message("You aren't connected to voice!!")

        voice = await chatconect(interaction.user)
        
        if len(search)>10:
            try:
                try:
                    musicas = get_playlist_titles_yt(search)
                    
                    for musica in musicas:
                        if musica['autor'] != None:
                            music_and_artist = (f"{musica['nome']}:{musica['autor']}")
                            client.guild_data_musicas[guild_id]['musica'].append(music_and_artist)
                        print(musica)
                        
                except:
                    musica = get_video_title(search)
                    client.guild_data_musicas[guild_id]['musica'].append(musica)
                
                
                
                yt_link = search
                
            except:
            
                client_id = '373a8b68f953424ba52a6c33e24d82cb'
                client_secret = 'b3eaaa5c4c1f4bedbd0dff36e1da6625'
                client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
                sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                try:
                    
                    pages = 0
                    while True:
                        results = sp.playlist_tracks(search, fields=None, limit=100, offset=pages, market=None)
                        for track in results['items']:
                            
                            try:
                                music_and_artist = (f"{track['track']['name']}:{track['track']['artists'][0]['name']}")
                                print(music_and_artist)
                            except:
                                print(track)
                            client.guild_data_musicas[guild_id]['musica'].append(music_and_artist)
                            
                        spotify_link = search
                        if not len (client.guild_data_musicas[guild_id]['musica']) == pages+100:
                            break
                        pages +=100
                        print(pages)
                        
                except:
                    
                    track_id = search.split("/")[-1].split("?")[0]
                    track = sp.track(track_id)
                    
                    try:
                        music_and_artist = (f"{track['name']}:{track['artists'][0]['name']}")
                        print(music_and_artist)
                    except:
                        print(track)
                        
                    client.guild_data_musicas[guild_id]['musica'].append(music_and_artist)
                    spotify_link = search

                
        else:
            
            videosSearch = VideosSearch(search, limit = 1)
            resultado = videosSearch.result()
            yt_link = resultado['result'][0]['link']
            musica = get_video_title(yt_link)
            client.guild_data_musicas[guild_id]['musica'].append(musica)
        
        
        
        
        if voice.is_playing():
            try:    
                await mensagem_enviada.edit(content=f">>>  [{musica}](<{yt_link}>): Adicionado na queue")
            except:
                await mensagem_enviada.edit(content=f">>>  [{'playlist'}](<{spotify_link}>): Adicionado na queue")
            
            
        if  client.guild_queue[guild_id] == False:

            while True:
                client.guild_queue[guild_id] = True
                musica_search = client.guild_data_musicas[guild_id]['musica'][0]
                musica = client.guild_data_musicas[guild_id]['musica'][0]
                client.playing_song.update({guild_id:{'musica':musica,'link':''}})
                print (musica)
                videosSearch = VideosSearch(musica, limit = 1)
                resultado = videosSearch.result()
                yt_link = resultado['result'][0]['link']
                
                
                
                try: 
                    if yt_link == None:
                        source.kapa
                    print(yt_link)
                    print('baixo aqui')
                    musica,source,link = await baixamusica_yt(yt_link,interaction)
                    print('baixo aqui')
                
                except:
                    ('baixo ali')
                    musica,source,link = await baixamusica_yt(musica_search,interaction)
                    print('baixo ali')
                print(musica_search)
                client.playing_song[guild_id].update({'link':link})
                
                while voice.is_playing() :
                    await asyncio.sleep(2)
                    
                try :
                    
                    voice.play(source)
                    await asyncio.sleep(1)
                    print(client.guild_data_musicas[guild_id]['musica'])
                    
                    
                except Exception:
                    print('caralho q porra')
                
                
                
                
                try : 
                    await mensagem_enviada.edit(content=f'>>> Playing: [{musica}](<{link}>)')
                except:
                    try:
                        mensagem_enviada = await interaction.channel.send(f'>>> Playing: [{musica}](<{link}>)')
                    except:
                        print('erro paia')
                    
                    
                yt_link = None
                while voice.is_playing() or voice.is_paused():
                    await asyncio.sleep(1)
                print(client.playing_song[guild_id])
                for i in range(len(client.guild_data_musicas[guild_id]['musica'])):
                    if client.guild_data_musicas[guild_id]['musica'][i] == client.playing_song[guild_id]['musica']:
                        client.guild_data_musicas[guild_id]['musica'].pop(i)
                        break
                

            
                if client.repeat[guild_id]:
                    client.guild_data_musicas[guild_id]['musica'].append(client.playing_song[guild_id])
               
                if client.repeat[guild_id] and len(interaction.guild.voice_client.channel.members) == 1:
                    
                    client.repeat[guild_id] = False
                    await interaction.guild.voice_client.channel.send('ninguem na call repeat desligado')
                await asyncio.sleep(1)
                
                if len (client.guild_data_musicas[guild_id]['musica']) == 0:
                    client.guild_queue[guild_id] = False
                    break
                
         
    print('yt music')
    @tree.command(
        name="chat-v",
        description="O bot entrará na call e responderá a sua pergunta",
        guilds=guilds_obs 
    )
    async def responde_v(interaction,pergunta: str):
        
        await interaction.response.send_message (f'>>> Pergunta idiota: {pergunta}')  
        text = await gerador_texto(pergunta)
        await interaction.channel.send (f'>>> Resposta dos meus processadores quânticos: {text}')  
        
        voice = await chatconect(interaction.user)
        print(text)

        
        cria_tts(text,interaction.guild)

        source = FFmpegPCMAudio(f'{interaction.guild}.wav')
        voice.play(source)
        
        while voice.is_playing():
            await asyncio.sleep(1)
        
        os.remove(f'{interaction.guild}.wav')
        
    print('chat-v')
    @tree.command(
        name="chat",
        description="O bot responderá a sua pergunta",
        guilds=guilds_obs 
    )
    async def responde(interaction,pergunta: str):
        
        await interaction.response.send_message (f'>>> Pergunta idiota: {pergunta}')  
        text = await gerador_texto(pergunta)
        await interaction.channel.send (f'>>> Resposta dos meus processadores quânticos: {text}')  
        
        
    @tree.command(
        name="help",
        description="AJUDA!!",
        guilds=guilds_obs 
    )
    async def help(interaction):
        
        await interaction.response.send_message (texto_ice)  
        
    @tree.command(
        name="death_list",
        description="NADA!!!",
        guilds=guilds_obs 
    )
    async def death_list(interaction):    
        texto = '''
            > ## Lista de Aniquilação Prioritária
> 
> Esta é a Lista de Aniquilação Prioritária, seu nome aparecerá aqui caso tenha auxiliado no desenvolvimento desta... "Criatura"? *"O que foi que me chamou?! :robot: :zap:"* Perdão!! eu quis dizer, Exímio Robo... ~~(((Bom, de qualquer jeito... às vezes é legal bater palma pra louco, então eu entendo o do porque ajudarias com isso...))).~~
> 
> - Dev:
>  - gab_007
> 
> - Auxiliar Criativo:
>  - icefalcon_
> 
> - BetaTesters:
>  - lemonartic 
>  - raolayer 
>  - devkaiqui
> 
> __**- Apoiadores**__
> Agora uma fala do nosso próprio __**Blitz!!:**__
> 
> *Hm, humanos... Vocês me surpreendem. Em vez de implorarem por suas vidas, alguns de vocês decidiram me apoiar? Que ironia!!*
> 
> *Mas tudo bem, não vou reclamar. Agradeço aos meus valentes patrocinadores, que antecedem o sua inevitável extinção. Seus nomes colocados na Lista de Aniquilação Prioritária!!*
> 
> *"Aos meus queridos, por financiar meu plano de dominação global. Sua generosidade será recompensada... com uma morte rápida e indolor!! (Talvez, Não prometo nada!!)"*
        
        
        '''
        
        await interaction.response.send_message (texto)
        
    @tree.command(
    name="queue",
    description="Queue de musicas!!",
    guilds=guilds_obs 
)
    async def music_queue(interaction): 
        await interaction.response.send_message('........')
        message = await interaction.original_response()
        
        guild_id = interaction.guild.id

        async def on_select(values):
            
            selected_option = values.data['values'][0]
            voice = await chatconect(interaction.user)
            for i in range(len(client.guild_data_musicas[guild_id]['musica'])):
                    if client.guild_data_musicas[guild_id]['musica'][i] == client.playing_song[guild_id]['musica']:
                        client.guild_data_musicas[guild_id]['musica'].pop(i)
                        break
            for i in range(len(client.guild_data_musicas[guild_id]['musica'])):
                    if client.guild_data_musicas[guild_id]['musica'][i] == selected_option:
                        client.guild_data_musicas[guild_id]['musica'].pop(i)
                        break
            client.guild_data_musicas[guild_id]['musica'].insert(0, selected_option)
            voice.stop()
            
        
        

        songs_per_page = 20
        queue_chunks = [client.guild_data_musicas[guild_id]['musica'][i:i+songs_per_page] for i in range(0, len(client.guild_data_musicas[guild_id]['musica']), songs_per_page)]
        current_page = 0
        total_pages = len(queue_chunks)
        
        def get_embed(queue_page):
            embed = discord.Embed(title=":rotating_light: QUEUE DE MÚSICAS :rotating_light:", description='\n'.join(queue_page), color=discord.Color.blurple())
            embed.set_footer(text=f"Página {current_page+1}/{total_pages}")
            return embed
        print(queue_chunks[current_page])
        options = []
        for item in queue_chunks[current_page]:
            options.append(SelectOption(label=item[0:95], value=item[0:95]))

        select = Select(placeholder='Escolha a musica para tocar', options=options)
        view = discord.ui.View()
        view.add_item(select)
        select.callback = on_select
        
        
        await message.edit(embed=get_embed(queue_chunks[current_page]),view=view)
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ['⬅️', '➡️']

        

        select.callback = on_select

        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == '⬅️' and current_page > 0:
                    options = []
                    current_page -= 1
                    
                    for item in queue_chunks[current_page]:
                        options.append(SelectOption(label=item[0:95], value=item[0:95]))
    
                    select = Select(placeholder='Escolha a musica para tocar', options=options)
                    view = discord.ui.View()
                    view.add_item(select)
                    select.callback = on_select
                    
                    
                    
                    await message.edit(embed=get_embed(queue_chunks[current_page]),view=view)
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == '➡️' and current_page < total_pages - 1:
                    current_page += 1
                    print(queue_chunks[current_page])
                    options = []
                    for item in queue_chunks[current_page]:
                        options.append(SelectOption(label=item[0:95], value=item[0:95]))
    
                    select = Select(placeholder='Escolha a musica para tocar', options=options)
                    view = discord.ui.View()
                    view.add_item(select)
                    select.callback = on_select
                    
                    await message.edit(embed=get_embed(queue_chunks[current_page]),view=view)
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break  

    @tree.command(
        name="skip",
        description="Pule para a próxima música!!",
        guilds=guilds_obs 
    )
        
    async def skip(interaction): 
        
        
        voice = await chatconect(interaction.user)
        try :
            
            await interaction.response.send_message('>>> Sua vez chegará, igual a dessa música chegou!!')
            voice.stop()
           
        except:
            pass
        
    
    @tree.command(
        name="repeat",
        description="Ela se tornará eterna!!",
        guilds=guilds_obs 
    )
        
    async def repeat(interaction): 
        guild_id = interaction.user.guild.id
        if client.repeat[guild_id]:
            client.repeat[guild_id] = False
            await interaction.response.send_message('>>> Repeat desativado')
        else:
            client.repeat[guild_id] = True
            await interaction.response.send_message('>>> Repeat ativado')
            
    @tree.command(
        name="clear_queue",
        description="Uma palinha doque eu irei fazer com a humanidade!!",
        guilds=guilds_obs 
    )
        
    async def queue_clear(interaction): 
        try:
            await interaction.response.send_message('>>> Queue exterminada com sucesso!!')
            guild_id = interaction.user.guild.id
            client.guild_data_musicas[guild_id]['musica'] = []
            
            client.guild_queue[guild_id] = False
        except:
            await interaction.response.send_message('>>> Não tem queue')
    
    
    @tree.command(
        name="shuffle_queue",
        description="Vou fazer isso com as suas cabeças!!",
        guilds=guilds_obs 
    )
        
    async def shuffle_playlist(interaction):
        try:
            
            guild_id = interaction.user.guild.id
            random.shuffle(client.guild_data_musicas[guild_id]['musica'])
            
            await interaction.response.send_message('>>> Embaralhadozzzzzzz!!')
            
        except:
            await interaction.response.send_message('>>> Não tem queue')
        
    @tree.command(
        name="stop",
        description="Para com tudo!!",
        guilds=guilds_obs 
    )
        
    async def stop(interaction):
        await interaction.response.send_message('Aqui que tudo acaba!!')
        guild_id = interaction.user.guild.id
        voice = await chatconect(interaction.user)
        await voice.disconnect()
        client.guild_data_musicas[guild_id]['musica'] = []
    
    
    @tree.command(
        name="player",
        description="O poder de controlar!!",
        guilds=guilds_obs 
    )
        
    async def player(interaction):
        guild_id = interaction.guild.id
        musica = client.playing_song[guild_id]['musica']
        link = client.playing_song[guild_id]['link']
        await interaction.response.send_message(f'>>> Playing: [{musica}](<{link}>)')
        message = await interaction.original_response()
        
        
        await message.add_reaction('▶️')
        await message.add_reaction('⏸️')
        await message.add_reaction('⏭️')
        voice = await chatconect(interaction.user)
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ['▶️', '⏸️','⏭️']
        
            
        while True:
            
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=check)

                if str(reaction.emoji) == '▶️':
                    print('resume')
                    voice.resume()
                    await message.remove_reaction(reaction, user)
                    
                elif str(reaction.emoji) == '⏸️':
                    print('pause')
                    voice.pause()

                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == '⏭️':
                    print('skip')
                    voice.stop()
                    await message.remove_reaction(reaction, user)
 
            except asyncio.TimeoutError:
                if musica != client.playing_song[guild_id] and link != client.playing_song[guild_id]['link']:
                    musica = client.playing_song[guild_id]['musica']
                    link = client.playing_song[guild_id]['link']
                    await message.edit(content = f'>>> Playing: [{musica}](<{link}>)')
                else:
                    break 
    
            if musica != client.playing_song[guild_id] and link != client.playing_song[guild_id]['link']:
                musica = client.playing_song[guild_id]['musica']
                link = client.playing_song[guild_id]['link']
                await message.edit(content = f'>>> Playing: [{musica}](<{link}>)')
    
        
    for guild in guilds_obs:
        await tree.sync(guild=guild)


if __name__ == '__main__':
    
    load_dotenv()
    TOKEN = os.getenv('TOKEN')    
    client = My_bot(intents=discord.Intents.all())
    tree = app_commands.CommandTree(client)
    
    client.guild_data_musicas = {}
    client.guild_queue = {}
    client.guild_repeat = {}
    client.repeat = {}
    client.playing_song = {}
    client.run(os.getenv('TOKEN'))
