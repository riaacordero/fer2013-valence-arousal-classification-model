const downloadButton = document.querySelector('.download-copy');


//download button
downloadButton.addEventListener('click', function() {
    let csv = [];
    let rows = document.querySelectorAll('.table-container #log-table div');

    for (let i = 0; i < rows.length; i++) {
        let row = [], cols = rows[i].querySelectorAll('div');

        for (let j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }

        // add image url
        row.push(rows[i].dataset.imageUrl)

        if (row.length === 0) {
            // do not include empty row!
            continue;
        }

        // trim whitespaces in comma-separated values
        csv.push(row.join(',').replace(', ', ','));
    }

    // Create and download the CSV file
    let csvFile = new Blob([csv.join('\n')], {type: 'text/csv'});
    let downloadLink = document.createElement('a');

    // Get the video file name from the URL
    let urlParams = new URLSearchParams(window.location.search);
    let source = urlParams.get('source');
    let videoName = source.substring(source.lastIndexOf('/') + 1, source.lastIndexOf('.'));

    downloadLink.download = videoName + '_data' + '.csv';
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);

    downloadLink.click();
});
