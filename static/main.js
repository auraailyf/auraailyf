document.addEventListener('DOMContentLoaded', () => {
    // ... (all your other existing JS code for navbar, scroll effects, etc.) ...
    // Keep all your original code from lines 1 to 65 here.
    // The new code is added below.
    
    // --- 5. Contact Form Submission with Debugging ---
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.querySelector('span').textContent;

        contactForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            submitButton.disabled = true;
            submitButton.querySelector('span').textContent = 'Sending...';

            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData.entries());

            // --- DEBUGGING ---
            const backendUrl = '/api/contact';
            console.log('--- Submitting Form ---');
            console.log('Attempting to POST to URL:', backendUrl);
            console.log('Data being sent:', JSON.stringify(data, null, 2));
            // --- END DEBUGGING ---

            try {
                const response = await fetch(backendUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                const result = await response.json();

                if (response.ok) {
                    alert('Success! Your message has been sent successfully.');
                    contactForm.reset();
                } else {
                    alert(`Error: ${result.error || 'Something went wrong.'}`);
                }
            } catch (error) {
                // --- MORE DEBUGGING ---
                console.error('Fetch failed with an error:', error);
                alert('Failed to connect to the server. Please check your connection and the browser console (F12) for more details.');
                // --- END DEBUGGING ---
            } finally {
                submitButton.disabled = false;
                submitButton.querySelector('span').textContent = originalButtonText;
            }
        });
    }
});
