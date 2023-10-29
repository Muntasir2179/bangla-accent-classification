import librosa
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

# function to add noise to original sound
def add_white_noise(signal, noise_factor):
    noise = np.random.normal(0, signal.std(), signal.size)
    augmented_signal = signal + noise * noise_factor
    return augmented_signal


# scaling the pitch
def pitch_scale(signal, sr, num_semitones):
    return librosa.effects.pitch_shift(y=signal, sr=sr, n_steps=num_semitones)


# invert polarity
def invert_polarity(signal):
    return signal * -1


def random_gain(signal, min_gain_factor, max_gain_factor):
    gain_factor = np.random.uniform(min_gain_factor, max_gain_factor)
    return signal * gain_factor


def plot_signal_and_augmented_signal(signal, augmented_signal, sr):
    fig, ax = plt.subplots(nrows=2)
    librosa.display.waveshow(signal, sr=sr, ax=ax[0])
    ax[0].set(title="Original signal")
    librosa.display.waveshow(augmented_signal, sr=sr, ax=ax[1])
    ax[1].set(title="Augmented signal")
    plt.show()


def augment_audio(signal, sr, noise_factor=0.05, num_semitones=0.5, min_gain_factor=2, max_gain_factor=4):
    augmented_signal = add_white_noise(signal, noise_factor)
    augmented_signal = pitch_scale(augmented_signal, sr, num_semitones)
    augmented_signal = invert_polarity(augmented_signal)
    augmented_signal = random_gain(augmented_signal, min_gain_factor, max_gain_factor)
    return augmented_signal

if __name__ == "__main__":
    signal, sr = librosa.load('chottgram_audio_97.wav')

    augmented_signal = augment_audio(signal, sr, noise_factor=0.05, num_semitones=0.5, min_gain_factor=2, max_gain_factor=4)

    sf.write('augmented.wav', augmented_signal, sr)
    plot_signal_and_augmented_signal(signal=signal, augmented_signal=augmented_signal, sr=sr)
