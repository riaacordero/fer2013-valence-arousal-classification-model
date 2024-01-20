
document.querySelector('.download-copy').addEventListener('click', function() {
    let csv = [];
        let rows = document.querySelectorAll('.table-container #log-table div');
    
        for (let i = 0; i < rows.length; i++) {
            let row = [], cols = rows[i].querySelectorAll('div');
    
            for (let j = 0; j < cols.length; j++) 
                row.push(cols[j].innerText);
    
            csv.push(row.join(','));        
        }
    
        // Create and download the CSV file
        let csvFile = new Blob([csv.join('\n')], {type: 'text/csv'});
        let downloadLink = document.createElement('a');
        downloadLink.download = 'data.csv';
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
}); 
    