# 🗣️ Offline Voice Recognition App (Python)

A lightweight Python application that performs **offline speech recognition** using local audio processing libraries.  
No internet connection is required – built entirely on open-source tools like **SpeechRecognition** and **CMU Sphinx**.

---

## ✨ Features

- 🔒 Fully offline speech-to-text processing
- 🎙️ Real-time or pre-recorded audio file transcription
- 🧠 Powered by CMU PocketSphinx (local model)
- 📦 Simple REST API using Flask for integration with other platforms (e.g., Flutter)

---

## 🛠️ Tech Stack

| Layer       | Technology          |
|-------------|---------------------|
| Programming | Python               |
| Speech Engine | CMU Sphinx (via `SpeechRecognition`) |
| API         | Flask (optional REST layer) |
| Audio Format| WAV (mono, 16-bit PCM) |

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- `pip` package manager

---

### 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/python-offline-voice.git
cd python-offline-voice

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

Project Structure
python-offline-voice/
│
├── app.py                  # Flask app for REST API
├── recognize_file.py       # CLI tool for WAV transcription
├── recognizer.py           # Core speech recognition logic
├── requirements.txt
└── README.md

