# from PIL import Image

# image = Image.open('barishal_audio_01.png')
# width, height = image.size
# print(str(width) + ' x ' + str(height))


# check metadata
import pandas as pd

metadata = pd.read_csv('spectrogram_metadata.csv')
print(len(metadata))
