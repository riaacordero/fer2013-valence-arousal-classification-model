// table.js

document.querySelector('.table-container table tbody')
    .addEventListener('click', function (e) {
        if (e.target.tagName.toLowerCase() === 'td') {
            const newRow = document.createElement('tr');
            const timestamp = new Date();
            const formattedTime = timestamp.getHours() + ":" + timestamp.getMinutes() + ":" + timestamp.getSeconds();

            newRow.innerHTML = '<td>' + formattedTime + '</td><td>Panic attack precursor detected!</td>';
            this.appendChild(newRow);

            // Add the following code to send the data to the server when a panic attack precursor is detected
            fetch('http://0.0.0.0:3000/update-content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `timestamp=${formattedTime}&message=Panic attack precursor detected!`,
            })
                .then(response => response.text())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error));
        }
    });
