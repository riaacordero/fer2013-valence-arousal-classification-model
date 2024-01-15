/** @type {HTMLCanvasElement} */
const rect = document.getElementById('rect');
const rectCtx = rect.getContext('2d');

function clearCanvas() {
    rectCtx.clearRect(0, 0, rect.width, rect.height);
}

function renderBoundingBox(bbox, valence, arousal, emotion) {
    // draw only if bbox is not empty and not 0
    if (!bbox || bbox[1] == 0 || bbox[2] == 0) {
        return;
    }

    // draw to canvas
    rectCtx.strokeStyle = '#04DC5B';
    rectCtx.lineWidth = 2;
    rectCtx.strokeRect(bbox[0], bbox[1], bbox[2], bbox[3]); // x, y, width, height

    // draw valence and arousal texts
    rectCtx.fillStyle = '#04DC5B';
    rectCtx.fillRect(bbox[0] - 1, bbox[1] - 20, 115, 20);

    rectCtx.font = '14px Arial';
    rectCtx.fillStyle = 'white';
    rectCtx.fillText(`V: ${valence.toFixed(2)}, A: ${arousal.toFixed(2)}`, bbox[0] + 3, bbox[1] - 5);

    if (emotion) {
        rectCtx.fillStyle = 'blue';
        rectCtx.fillRect(bbox[0] - 1, bbox[1] + bbox[3] + 2, 80, 20);

        rectCtx.fillStyle = 'white';
        rectCtx.fillText(emotion, bbox[0] + 3, bbox[1] + bbox[3] + 15);
    }
}
