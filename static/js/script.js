document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.container');
    container.classList.add('fade-in');
    setTimeout(() => container.classList.add('visible'), 100);
});