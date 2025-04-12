document.addEventListener("DOMContentLoaded", function () {
    const transcriptionBox = document.getElementById("transcription");

    function startRecording() {
        fetch("/start_recording")
            .then(response => response.json())
            .then(data => {
                transcriptionBox.value = "Listening...";
            })
            .catch(error => console.error("Error:", error));
    }

    function stopRecording() {
        fetch("/stop_recording")
            .then(response => response.json())
            .then(data => {
                transcriptionBox.value = data.text;
            })
            .catch(error => console.error("Error:", error));
    }

    function downloadText() {
        window.location.href = "/download_text";
    }

    // Attach event listeners
    document.getElementById("startBtn").addEventListener("click", startRecording);
    document.getElementById("stopBtn").addEventListener("click", stopRecording);
    document.getElementById("downloadBtn").addEventListener("click", downloadText);
});
