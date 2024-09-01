document.addEventListener('mousemove', (event) => {
    const x = event.clientX;
    const y = event.clientY;
    const gradientSize = 150; // Size of the fading effect
    const fadeOpacity = 0.4; // Darker fade with higher opacity
    
    // Update the overlay's gradient based on mouse position
    const overlay = document.getElementById('fade-overlay');
    overlay.style.background = `
        radial-gradient(circle at ${x}px ${y}px, rgba(0, 0, 0, ${fadeOpacity}), transparent ${gradientSize}px)
    `;
});

// Reset the overlay when the mouse leaves the window
document.addEventListener('mouseleave', () => {
    const overlay = document.getElementById('fade-overlay');
    overlay.style.background = `
        radial-gradient(circle at 0 0, rgba(0, 0, 0, 0.7), transparent 150px)
    `;
});
