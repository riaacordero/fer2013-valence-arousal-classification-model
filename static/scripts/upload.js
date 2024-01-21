const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');

// Disable the upload button by default
uploadButton.disabled = true;
console.log(uploadButton.disabled); // check

fileInput.addEventListener('change', function() {
    // If a file is selected, enable the upload button, otherwise disable it
    uploadButton.disabled = fileInput.files.length === 0;
});

document.querySelector('form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const file = document.querySelector('input[type="file"]').files[0];
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/uploadvideo/', {method: 'POST', body: formData});
    
    if (!response.ok) {
        console.error('Upload request failed');
        return;
    }

    const data = await response.json();

    if (!data.filename) {
        console.error('Filename not provided in the server response');
        return;
    }

    const newUrl = `http://localhost:3000/?source=/test_files/test_video/${data.filename}`;
    window.location.href = newUrl;
});