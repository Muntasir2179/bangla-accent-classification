import pandas as pd

dataset = pd.read_csv('augmented_audio_trace_metadata.csv')

print(dataset.head())
print(dataset['accent'].unique())
print(len(dataset))