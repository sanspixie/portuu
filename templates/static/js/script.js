// Contact form validation
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            let errorMsg = '';

            if (name.length < 2) errorMsg += 'Name must be at least 2 characters.\n';
            if (!email.includes('@')) errorMsg += 'Enter a valid email.\n';
            if (message.length < 10) errorMsg += 'Message must be at least 10 characters.\n';

            if (errorMsg) {
                e.preventDefault();
                alert(errorMsg);
            }
        });
    }
});
