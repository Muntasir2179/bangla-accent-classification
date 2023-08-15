import os
from csv import writer
import pandas as pd

folder_names = os.listdir()

folder_names.remove('.vscode')
folder_names.remove('meteadata_generator.py')
folder_names.remove('resolution_checker.py')
folder_names.remove('spectrogram_generator.py')

# print(folder_names)
# print(len(folder_names))

# data = pd.read_csv('metadata.csv')

# print(len(data))

with open('spectrogram_metadata.csv', 'w', encoding='utf8', newline='') as f:
    csv_writer = writer(f)
    header = ['file_name', 'folder_name', 'accent']
    csv_writer.writerow(header)

    for folder in folder_names:
        files = os.listdir(os.path.join(folder))
        for file in files:
            csv_writer.writerow([file, folder, folder])

f.close()
