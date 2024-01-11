

document.querySelector('.table-container table tbody')
    .addEventListener('click', function(e) {
        if (e.target.tagName.toLowerCase() === 'td') {
            const newRow = document.createElement('tr');
            const timestamp = new Date();
            const formattedTime = timestamp.getHours() + ":" + timestamp.getMinutes() + ":" + timestamp.getSeconds();

            newRow.innerHTML = '<td>' + formattedTime + '</td><td>Panic attack precursor detected!</td>';
            this.appendChild(newRow);
        }
    }
);