// Add your custom JavaScript here
console.log("JavaScript loaded!");
const videoElement = document.getElementById("video");
const startCameraBtn = document.getElementById("startCamera");
const stopCameraBtn = document.getElementById("stopCamera");
const fileInput = document.getElementById("fileInput");
let stream;

// Activate camera
startCameraBtn.addEventListener("click", async () => {
  try {
    const response = await fetch('/start_camera', { method: 'POST' });
    if (response.ok) {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoElement.srcObject = stream;
      videoElement.hidden = false;
      startCameraBtn.disabled = true;
      stopCameraBtn.disabled = false;

      // Iniciar la captura de predicciones en tiempo real
      const eventSource = new EventSource('/live_prediction');
      eventSource.onmessage = function(event) {
        document.getElementById('predictedText').innerText = event.data;
      };
    } else {
      alert("Failed to activate camera.");
    }
  } catch (err) {
    alert("Camera access denied or unavailable.");
    console.error(err);
  }
});

// Stop camera
stopCameraBtn.addEventListener("click", async () => {
  try {
    const response = await fetch('/stop_camera', { method: 'POST' });
    if (response.ok) {
      if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach((track) => track.stop());
        videoElement.hidden = true;
        startCameraBtn.disabled = false;
        stopCameraBtn.disabled = true;

        // Detener la captura de predicciones en tiempo real
        const eventSource = new EventSource('/live_prediction');
        eventSource.close();
        document.getElementById('predictedText').innerText = "";
      }
    } else {
      alert("Failed to deactivate camera.");
    }
  } catch (err) {
    alert("Failed to deactivate camera.");
    console.error(err);
  }
});

// Load video file
fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    const url = URL.createObjectURL(file);
    videoElement.src = url;
    videoElement.hidden = false;
    startCameraBtn.disabled = true;
    stopCameraBtn.disabled = true;
  }
});
