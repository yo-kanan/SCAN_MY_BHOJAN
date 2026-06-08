document.addEventListener('DOMContentLoaded', () => {
    const splashScreen = document.getElementById('splash-screen');
    const splashVideo = document.getElementById('splash-video');
    const bgVideo = document.getElementById('bg-video');

    // Ensure the splash video plays (sometimes browsers block autoplay)
    splashVideo.play().catch(error => {
        console.error("Splash video autoplay failed:", error);
    });

    // Event Listener: When splash video finishes playing
    splashVideo.addEventListener('ended', () => {
        
        // 1. Add the CSS class to fade opacity to 0
        splashScreen.classList.add('fade-out');

        // 2. Ensure the main background video is playing
        bgVideo.play();

        // 3. Optional: Remove the splash screen from DOM entirely after fade is done (1.5s)
        setTimeout(() => {
            splashScreen.style.display = 'none';
        }, 1500); // Matches the transition time in CSS
    });
});