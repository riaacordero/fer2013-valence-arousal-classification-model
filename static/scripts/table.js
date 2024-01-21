// table.js
function logItem(result) {
    const timestamp = result.timestamp;
    const message = result.result;
    if (!timestamp || !message) {
        return;
    }

    const image = result.image;

    // timestamp
    const timestampDiv = document.createElement('div');
    timestampDiv.innerText = timestamp;

    // message
    const messageDiv = document.createElement('div');
    messageDiv.innerText = message;

    const tableEntry = document.createElement('div');
    tableEntry.className = 'table-entry';
    tableEntry.dataset.imageUrl = image;
    tableEntry.addEventListener('click', function (e) {
        // 1. render image in canvas
        if (!image) {
            return;
        }

        // create an image canvas
        const imageCanvas = document.createElement('canvas');
        imageCanvas.width = videoCanvas.width;
        imageCanvas.height = videoCanvas.height;

        // draw image to canvas
        const imageCtx = imageCanvas.getContext('2d');
        const imageStream = new Image(videoCanvas.width, videoCanvas.height);
        imageStream.src = image;
        imageStream.onload = function() {
            // if this code is executed outside, it will only display a transparent canvas
            // because the image is not yet loaded. so we need to wait for the image to load

            // draw image to canvas
            imageCtx.drawImage(imageStream, 0, 0);

            // 2. render bounding box
            renderBoundingBox(imageCtx, result.bbox, result.valence, result.arousal, result.emotion);

            // 3. open image in popup window
            const popup = window.open('', 'Image', `width=${videoCanvas.width + 100},height=${videoCanvas.height + 100}`);
            // center window
            popup.moveTo((screen.width - (videoCanvas.width + 100)) / 2, (screen.height - (videoCanvas.height + 100)) / 2);

            // render canvas to popup window
            popup.document.write('<img src="' + imageCanvas.toDataURL() + `" width="${imageCanvas.width}" height="${imageCanvas.height}">`);
        };
    })

    tableEntry.appendChild(timestampDiv);
    tableEntry.appendChild(messageDiv);

    const logTable = document.getElementById('log-table');
    logTable.appendChild(tableEntry);

    // scroll to bottom
    tableEntry.scrollIntoView();
}

document.querySelector('.table-container #log-table div')
    .addEventListener('click', function (e) {
        if (e.target.tagName.toLowerCase() === 'div') {
            const newRow = document.createElement('tr');
            const timestamp = new Date();
            const formattedTime = timestamp.getHours() + ":" + timestamp.getMinutes() + ":" + timestamp.getSeconds();

            newRow.innerHTML = '<div>' + formattedTime + '</div><div>Panic attack precursor detected!</div>';
            this.appendChild(newRow);

            // Add the following code to send the data to the server when a panic attack precursor is detected
            // fetch('http://0.0.0.0:3000/update-content', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/x-www-form-urlencoded',
            //     },
            //     body: `timestamp=${formattedTime}&message=Panic attack precursor detected!`,
            // })
            //     .then(response => response.text())
            //     .then(data => console.log(data))
            //     .catch(error => console.error('Error:', error));
        }
    });
