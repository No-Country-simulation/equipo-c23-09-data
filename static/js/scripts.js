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
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElement.srcObject = stream;
    videoElement.hidden = false;
    startCameraBtn.disabled = true;
    stopCameraBtn.disabled = false;
  } catch (err) {
    alert("Camera access denied or unavailable.");
    console.error(err);
  }
});

// Stop camera
stopCameraBtn.addEventListener("click", () => {
  if (stream) {
    const tracks = stream.getTracks();
    tracks.forEach((track) => track.stop());
    videoElement.hidden = true;
    startCameraBtn.disabled = false;
    stopCameraBtn.disabled = true;
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
