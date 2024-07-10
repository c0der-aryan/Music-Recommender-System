import time
import librosa
import matplotlib.pyplot as plt
import numpy as np

file_path_1  = "mp3_files/On My Way.wav"
file_path_2  = "mp3_files/In Control.wav"
def spectral_feat(file_path) :

    y , sr = librosa.load(file_path)

    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=2048, hop_length=512)[0]
    mel_spectogram = librosa.feature.melspectrogram(y=y , sr = sr  , n_fft = 2048 , hop_length=512, n_mels = 10)

    log_mel_spectogram = librosa.power_to_db(mel_spectogram)

    stft = np.abs(librosa.stft(y))

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Print the Spectral Centroid
    print('Spectral Centroid:', spectral_centroids)

    # Print the MFCCs
    print('MFCCs:', mfccs)

def time(file_path): 
    c = time.time()
    spectral_feat(file_path)
    f = time.time()
    print(f-c + "secs")

time(file_path_1)

time(file_path_2)
# plt.figure(figsize = (25,10))
# librosa.display.specshow(log_mel_spectogram,
#                             x_axis = "time",
#                             y_axis = "mel",
#                             sr = sr)
# plt.colorbar(format = "%+2.f")
# # plt.savefig(f"mp3_files/{song_info['name']}.png")
