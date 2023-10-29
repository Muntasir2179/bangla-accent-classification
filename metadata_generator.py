import os
from csv import writer

folder_names = os.listdir()

folder_names.remove('metadata_generator.py')
folder_names.remove('check.py')
folder_names.remove('audio_data_augmentation.py')
folder_names.remove('augmented_data_generator.py')

# print(folder_names)
# print(len(folder_names))

with open('augmented_audio_trace_metadata.csv', 'w', encoding='utf8', newline='') as f:
    csv_writer = writer(f)
    header = ['file_name', 'folder_name', 'accent']
    csv_writer.writerow(header)

    for folder in folder_names:
        files = os.listdir(os.path.join(folder))
        for file in files:
            csv_writer.writerow([file, folder, folder.replace(' augmented', '')])
f.close()
