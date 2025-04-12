import pytesseract
from PIL import Image
from flask import Flask, render_template, jsonify, send_file, request
import vosk
import sounddevice as sd
import queue
import json
import threading
from pydub import AudioSegment
import os
import pyttsx3

app = Flask(__name__)

q = queue.Queue()
recording = False
recognized_text = ""

# Use a larger Vosk model for better accuracy
MODEL_PATH = "model/vosk-model-small-en-in-0.4"
model = vosk.Model(MODEL_PATH)

tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)

def recognize_audio():
    """Recognizes speech from the microphone in real-time."""
    global recording, recognized_text
    samplerate = 16000
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)

        while recording:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                recognized_text += result.get("text", "") + " "
            else:
                partial_result = json.loads(rec.PartialResult())
                print("Partial:", partial_result.get("partial", ""))  # Debugging


def callback(indata, frames, time, status):
    """Puts microphone input into the queue."""
    if status:
        print(status)
    q.put(bytes(indata))


def reduce_noise(audio_path):
    """Reduces noise from the recorded audio file using a low-pass filter."""
    audio = AudioSegment.from_wav(audio_path)
    filtered_audio = audio.low_pass_filter(3000)  # Remove background noise
    filtered_audio.export("filtered_audio.wav", format="wav")
    return "filtered_audio.wav"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start_recording")
def start_recording():
    """Starts speech recognition in a separate thread."""
    global recording, recognized_text
    recording = True
    recognized_text = ""

    threading.Thread(target=recognize_audio, daemon=True).start()
    return jsonify({"text": "Listening..."})


@app.route("/stop_recording")
def stop_recording():
    """Stops the speech recognition process."""
    global recording
    recording = False
    return jsonify({"text": recognized_text})


@app.route("/download_text")
def download_text():
    """Saves the recognized text to a file and provides a download link."""
    global recognized_text
    filename = "converted_text.txt"
    with open(filename, "w") as f:
        f.write(recognized_text)
    return send_file(filename, as_attachment=True)


@app.route("/upload_image", methods=["POST"])
def upload_image():
    """Handles image-to-text conversion using Tesseract OCR."""
    print("Received request for image-to-text conversion")  # Debugging

    if "image" not in request.files:
        print("No file uploaded")  # Debugging
        return jsonify({"error": "No file uploaded"}), 400

    image = request.files["image"]
    if image.filename == "":
        print("No selected file")  # Debugging
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded image
    image_path = os.path.join("static", "uploaded_image.png")
    image.save(image_path)
    print("Image saved at:", image_path)  # Debugging

    # Convert image to text using Tesseract OCR
    text = pytesseract.image_to_string(Image.open(image_path))
    print("Extracted Text:", text)  # Debugging

    return jsonify({"text": text})


@app.route("/save_manual_text", methods=["POST"])
def save_manual_text():
    """Saves manually entered text to a file and allows downloading."""
    global manual_text
    manual_text = request.form.get("text", "")

    if not manual_text.strip():
        return jsonify({"error": "Text is empty"}), 400

    filename = "manual_text.txt"
    with open(filename, "w") as f:
        f.write(manual_text)

    return send_file(filename, as_attachment=True)

@app.route("/text_to_speech", methods=["POST"])
def text_to_speech():
    """Converts text to speech and returns an audio file."""
    text = request.form.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    output_audio = "static/speech_output.mp3"
    tts_engine.save_to_file(text, output_audio)
    tts_engine.runAndWait()

    return jsonify({"audio_url": output_audio})

if __name__ == "__main__":
    app.run(debug=True)
