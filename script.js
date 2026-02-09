document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', event => {
        event.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

const observer = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    },
    { threshold: 0.2 }
);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.section').forEach(section => observer.observe(section));

    const chips = document.querySelectorAll('.chip');
    const cards = document.querySelectorAll('.blog-card');

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const filter = chip.dataset.filter;
            chips.forEach(item => item.classList.remove('is-active'));
            chip.classList.add('is-active');

            cards.forEach(card => {
                const category = card.dataset.category;
                const isVisible = filter === 'all' || filter === category;
                card.style.display = isVisible ? 'block' : 'none';
            });
        });
    });
});
