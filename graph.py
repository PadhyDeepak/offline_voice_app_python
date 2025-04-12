import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from vosk import Model, KaldiRecognizer
import wave

import vosk

# Load the audio file
audio_path = "C:\\Users\\asus\\Desktop\\IMPORTANT\\OneDrive\\Documents\\Sound Recordings\\Recording (2).wav"

y, sr = librosa.load(audio_path, sr=16000)

# Calculate MFCC
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# Plotting the Raw Audio Waveform
plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
librosa.display.waveshow(y, sr=sr)
plt.title("Raw Audio Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# Plotting the MFCCs
plt.subplot(3, 1, 2)
librosa.display.specshow(mfccs, sr=sr, x_axis='time')
plt.colorbar(format='%+2.0f dB')
plt.title("MFCC (Mel-frequency Cepstral Coefficients)")
plt.xlabel("Time (s)")
plt.ylabel("MFCC Coefficients")

# Vosk Model Speech Recognition Results
wf = wave.open(audio_path, "rb")
model_path = r"C:\Users\asus\Downloads\vosk-model-small-en-us-0.15\vosk-model-small-en-us-0.15"
model = vosk.Model(model_path)
rec = KaldiRecognizer(model, wf.getframerate())

results = []
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        results.append(result)

# Display Results
plt.subplot(3, 1, 3)
result_text = "\n".join([r for r in results])
plt.text(0.1, 0.5, result_text, fontsize=12)
plt.axis('off')
plt.title("Vosk Model Recognition Results")

plt.tight_layout()
plt.show()
