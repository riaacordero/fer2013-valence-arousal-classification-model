const playPauseButton = document.getElementById('playPauseButton');

// playPauseButton.addEventListener('click', function() {
//     if (videoStream.paused) {
//         videoStream.play();
//     } else {
//         videoStream.pause();
//     }
// });

playPauseButton.addEventListener('click', function() {
    if (videoStream.paused) {
        videoStream.play();
        playPauseButton.innerHTML = '<span class="material-symbols-outlined">pause</span>'; // Change to pause symbol
    } else {
        videoStream.pause();
        playPauseButton.innerHTML = '<span class="material-symbols-outlined">play_arrow</span>'; // Change to play symbol
    }
});