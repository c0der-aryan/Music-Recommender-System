import os

from pytube import YouTube
from  pytube import Search 
from pydub import AudioSegment


import librosa
import matplotlib.pyplot as plt

song_info = {'acousticness': 0.0209,
 'artists': ['Alan Walker', 'Sabrina Carpenter', 'Farruko'],
 'danceability': 0.509,
 'energy': 0.689,
 'explicit': True,
 'instrumentalness': 0,
 'languages': ['en', 'es'],
 'liveness': 0.301,
 'loudness': -4.929,
 'lyrics': "I'm sorry but Don't wanna talk I need a moment before I go It's "
           "nothing personal I draw the blinds They don't need to see me cry "
           "'Cause even if they understand They don't understand So then when "
           "I'm finished I'm all 'bout my business And ready to save the world "
           "I'm takin' my misery Make it my bitch Can't be everyone's "
           "favourite girl So, take aim and fire away I've never been so wide "
           "awake No, nobody but me can keep me safe And I'm on my way The "
           'blood moon is on the rise The fire burning in my eyes No, nobody '
           "but me can keep me safe And I'm on my way ♪ Lo siento mucho "
           '(Farru) Pero me voy (eh) Porque a tu lado me di cuenta que nada '
           'soy (eh-eh) Y me cansé de luchar y de guerrear en vano De estar en '
           'la línea de fuego y de meter la mano Acepto mis errores, también '
           'soy humano Y tú no ve que lo hago porque te amo (pum-pum-pum-pum) '
           'Pero ya (ya) No tengo más na que hacer aquí (aquí) Me voy, llegó '
           'la hora de partir (partir) De mi propio camino, seguir lejos de ti '
           "So, take aim and fire away I've never been so wide awake No, "
           "nobody but me can keep me safe And I'm on my way The blood moon is "
           'on the rise (is on the rise, na-na) The fire burning in my eyes '
           '(the fire burning in my eyes, na) No, nobody but me can keep me '
           "safe And I'm on my way ♪ (I'm on my way) (Ever... everybody keep "
           'me safe) (Ever... everybody keep me safe) (Ever... everybody keep '
           'me safe) (Ever... everybody) (Everybody on my way) So, take aim '
           "and fire away I've never been so wide awake No, nobody but me can "
           "keep me safe And I'm on my way The blood moon is on the rise The "
           "fire burning in my eyes No, nobody but me can keep me safe And I'm "
           'on my way ',
 'name': 'On My Way',
 'sentiments': [0.511660099029541, 0, 0.4057457447052002, 0, 0, 0, 0],
 'tempo': 170.087}


def convert_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    destination = "wav_files/"
    wav_output_path = destination + '.wav'
    audio.export(wav_output_path, format='wav')
    return wav_output_path


def ytb_url_to_mp3 (url) : 
    song_ytb_search =  (song_info["name"] + " " + ", ".join(song_info["artists"]))
    s = Search(song_ytb_search)
    first_result = s.results[0]
    url = f"https://www.youtube.com/watch?v={first_result.video_id}"

    yt = YouTube(url)
    video = yt.streams.filter(only_audio = True).first()
    destination = "mp3_files/"
    out_file = video.download(output_path = destination) 
    base , _  = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file , new_file)
    return new_file

def ytb_url_to_wav (url) : 
    file_path = ytb_url_to_mp3(url)

    return new_file

def get_mel_spec(song_info) : 
    file_path = ytb_url_to_wav(song_info)

    y , sr = librosa.load(file_path)
    mel_spectogram = librosa.feature.melspectrogram(y=y , sr = sr , n_fft = 2048 , hop_length=512, n_mels = 10, )
    log_mel_spectogram = librosa.power_to_db(mel_spectogram)

    plt.figure(figsize = (25,10))
    librosa.display.specshow(log_mel_spectogram,
                            x_axis = "time",
                            y_axis = "mel",
                            sr = sr)
    plt.colorbar(format = "%+2.f")
    plt.savefig(f"mp3_files/{song_info['name']}.png")

get_mel_spec(song_info)
