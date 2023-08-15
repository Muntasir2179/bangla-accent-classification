import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import os

# image libraries
from PIL import Image


# creating function to generate spectorgram of audio file
def generate_spectrogram(audio_file_path):
    # loading the audio file with librosa
    data, sample_rate = librosa.load(audio_file_path)

    # generating spectrogram
    spec = librosa.feature.melspectrogram(y=data, sr=sample_rate)
    spec_db = librosa.power_to_db(spec, ref=np.max)

    # Resize the spectrogram to 224x224 pixels
    spec_resized = np.array(Image.fromarray(
        spec_db).resize((224, 224), Image.ANTIALIAS))

    # Display the resized spectrogram as an image
    plt.figure(figsize=(5, 5))
    plt.imshow(spec_resized, cmap='inferno', origin='lower')
    plt.axis('off')
    file_name = str(audio_file_path.split(
        '/')[-1].removesuffix('.wav')) + '.png'
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0)
    image = Image.open(file_name)
    image_resized = image.resize((224, 224))
    os.remove(file_name)
    image_resized.save(
        'D:/Bangla Accent Spectrogram Dataset/chottogram/' + file_name)


if __name__ == '__main__':
    file_path = 'D:/Bangla Accent Dataset/chottogram/chottgram_audio_0'
    flag = True

    for i in range(1, 101):
        if flag and i > 9:
            file_path = file_path.replace(file_path[-1], '')
            flag = False
        new_path = file_path + str(i) + '.wav'
        generate_spectrogram(new_path)
