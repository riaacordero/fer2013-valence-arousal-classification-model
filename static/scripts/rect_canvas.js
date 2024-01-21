/** @type {HTMLCanvasElement} */
const rect = document.getElementById('rect');
const rectCtx = rect.getContext('2d');

function clearCanvas() {
    rectCtx.clearRect(0, 0, rect.width, rect.height);
}

function renderBoundingBox2(bbox, valence, arousal, emotion) {
    return renderBoundingBox(rectCtx, bbox, valence, arousal, emotion);
}

function renderBoundingBox(ctx, bbox, valence, arousal, emotion) {
    // draw only if bbox is not empty and not 0
    if (!bbox || bbox[1] == 0 || bbox[2] == 0) {
        return;
    }

    // draw to canvas
    ctx.strokeStyle = '#04DC5B';
    ctx.lineWidth = 2;
    ctx.strokeRect(bbox[0], bbox[1], bbox[2], bbox[3]); // x, y, width, height

    // draw valence and arousal texts
    ctx.fillStyle = '#04DC5B';
    ctx.fillRect(bbox[0] - 1, bbox[1] - 20, 115, 20);

    ctx.font = '14px Arial';
    ctx.fillStyle = 'white';
    ctx.fillText(`V: ${valence.toFixed(2)}, A: ${arousal.toFixed(2)}`, bbox[0] + 3, bbox[1] - 5);

    if (emotion) {
        ctx.fillStyle = 'blue';
        ctx.fillRect(bbox[0] - 1, bbox[1] + bbox[3] + 2, 80, 20);

        ctx.fillStyle = 'white';
        ctx.fillText(emotion, bbox[0] + 3, bbox[1] + bbox[3] + 15);
    }
}
