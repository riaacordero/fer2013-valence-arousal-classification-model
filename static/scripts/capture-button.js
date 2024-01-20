// Load the capture button when the window is loaded.
window.onload = function() {
    let captureButton = document.getElementById("captureButton");

    captureButton.addEventListener("click", function() {
        let videoCanvas = document.querySelector('#video');
        let rectCanvas = document.querySelector('#rect');

        if (videoCanvas && rectCanvas) {
            let context = videoCanvas.getContext('2d');

            // Draw the rect canvas onto the video canvas.
            context.drawImage(rectCanvas, 0, 0);

            // Create a data URL from the video canvas.
            let dataURL = videoCanvas.toDataURL('image/png');

            // Create a link element.
            let link = document.createElement('a');

            // Set the link's href to the data URL.
            link.href = dataURL;

            // Set the download attribute to the desired file name.
            link.download = 'screenshot.png';

            // Trigger a click event on the link to start the download.
            link.click();
        } else {
            console.error('Canvas not found');
        }
    });
};