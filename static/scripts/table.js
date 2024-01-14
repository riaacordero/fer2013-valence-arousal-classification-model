// table.js
function logItem(timestamp, message) {
    if (!timestamp || !message) {
        return;
    }

    // timestamp
    const timestampDiv = document.createElement('div');
    timestampDiv.innerText = timestamp;

    // message
    const messageDiv = document.createElement('div');
    messageDiv.innerText = message;

    const tableEntry = document.createElement('div');
    tableEntry.className = 'table-entry';

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
