import os
import pandas as pd
import librosa
from tqdm import tqdm
import audio_data_augmentation as aug
import soundfile as sf


if __name__ == "__main__":
    metadata_path = 'D:/Bangla Accent Dataset/audio_trace_metadata.csv'
    metadata = pd.read_csv(metadata_path)

    class_labels = metadata['accent'].unique()

    # creating folders
    for i, accent in enumerate(class_labels):
        if not os.path.exists(f"{accent} augmented"):
            os.mkdir(f"{accent} augmented")

    # reading original audio and applying augmentation
    for index_num, row in tqdm(metadata.iterrows()):
        accent_label = row['accent']
        file_path = 'D:/Bangla Accent Dataset' + str('/') + str(row['folder_name']) + '/' + str(row['file_name'])
        signal, sr = librosa.load(file_path, res_type='kaiser_fast')
        augmented_audio = aug.augment_audio(signal=signal, sr=sr)
        file_name = str(row['file_name']).replace('.wav', '')
        sf.write(f'D:/Bangla Accent Dataset Augmented/{row["folder_name"]} augmented/{file_name}_augmented.wav', augmented_audio, sr)