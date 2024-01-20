/** @type {HTMLCanvasElement} */
const videoCanvas = document.getElementById('video');
const videoCtx = videoCanvas.getContext('2d');
const videoStream = document.createElement('video');

videoStream.autoplay = true;
videoStream.playsInline = true;
videoStream.loop = true;
videoStream.muted = true;
videoStream.addEventListener('play', () => {
    function step() {
        if (!videoCanvas || !videoCtx) return;
        videoCtx.drawImage(videoStream, 0, 0, videoCanvas.width, videoCanvas.height);
        requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
});

/**
 *
 * @param {string | 0 | MediaStream} source
 */
function videoCapture(source) {
    console.log('Loading video stream...', source);

    if ((typeof source == 'number' || (typeof source == 'string' && source.length != 0)) && source == 0) {
        // get webcam stream similar to cv2.VideoCapture(0)
        navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        })
            .then(videoCapture)
            .catch(console.error);
    } else if (typeof source === 'string') {
        videoStream.src = source;
        videoStream.load();
    } else {
        videoStream.srcObject = source;
    }

    videoStream.play();
}

function snapshotVideo() {
    return videoCanvas.toDataURL('image/jpeg', 0.8);
}
