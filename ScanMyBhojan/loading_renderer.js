document.addEventListener('DOMContentLoaded', () => {
    const splashVideo = document.getElementById('splash-video');
    
    // Attempt to play the video (Electron generally allows autoplay)
    splashVideo.play().catch(error => {
        console.error("Splash video autoplay failed:", error);
    });

    // Event Listener: When splash video finishes playing
    splashVideo.addEventListener('ended', () => {
        console.log("Splash video finished. Navigating to index.html...");
        
        // This is the key line: it changes the entire window's content to index.html
        window.location.href = 'index.html';
    });

    // Fallback: If for some reason the video doesn't end (e.g., file error),
    // navigate after a max timeout (optional but safe)
    setTimeout(() => {
        if (window.location.pathname.endsWith('loading.html')) {
            console.warn("Timeout reached. Navigating to index.html as fallback.");
            window.location.href = 'index.html';
        }
    }, 5000); // 5 second maximum wait time
});