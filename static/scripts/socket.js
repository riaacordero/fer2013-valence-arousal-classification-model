const ws = new WebSocket('ws://' + window.location.host + '/session');

ws.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (data.result) {
        const result = data.result;
        if (data.command === 'analyze') {
            // log result
            logItem(result.timestamp, result.result);

            // draw bounding box
            clearCanvas();
            renderBoundingBox(result.bbox, result.valence, result.arousal);
        }
    } else if (data.message) {
        console.log(data.type, data.message);
    }
}

function isConnected() {
    return ws.readyState == ws.OPEN;
}

function sendCommand(command, params = {}) {
    if (!isConnected()) {
        return;
    }
    ws.send(JSON.stringify({ command, params }));
}

function closeConnection() {
    if (!isConnected()) {
        return;
    }
    sendCommand('close');
    ws.close();
}

