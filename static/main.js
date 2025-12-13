document.addEventListener('DOMContentLoaded', () => {
    // --- (Your existing code for navbar, scroll effects, etc. goes here) ---
    // This section should contain all the visual effects for your page.
    // For this example, I'll assume your previous code is here.

    // --- 5. Contact Form Submission Logic ---
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.querySelector('span').textContent;

        contactForm.addEventListener('submit', async (event) => {
            // Prevent the browser's default behavior of reloading the page on submit
            event.preventDefault();

            // Provide visual feedback to the user
            submitButton.disabled = true;
            submitButton.querySelector('span').textContent = 'Sending...';

            // Collect all the data from the form fields
            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData.entries());

            // --- THIS URL IS CORRECT ---
            // Using a relative URL like '/api/contact' is the best practice.
            // It works for both your local server (http://127.0.0.1:5000)
            // and your live Render server (https://auraailyf.onrender.com).
            const backendUrl = '/api/contact';
            
            console.log('--- Submitting Form ---');
            console.log('Attempting to POST to URL:', backendUrl);
            console.log('Data being sent:', JSON.stringify(data, null, 2));

            try {
                // Send the data to the backend using the Fetch API
                const response = await fetch(backendUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                const result = await response.json();

                if (response.ok) {
                    // If the backend responds with success, show an alert and clear the form
                    alert('Success! Your message has been sent successfully.');
                    contactForm.reset();
                } else {
                    // If the backend responds with an error, show the error message
                    alert(`Error: ${result.error || 'Something went wrong.'}`);
                }
            } catch (error) {
                // This catches network errors (e.g., server is down)
                console.error('Fetch failed with an error:', error);
                alert('Failed to connect to the server. Please check your connection and the browser console (F12) for more details.');
            } finally {
                // Always re-enable the button, whether it succeeded or failed
                submitButton.disabled = false;
                submitButton.querySelector('span').textContent = originalButtonText;
            }
        });
    }
});

function closePopup() {
            const popup = document.getElementById('promoPopup');
            popup.style.opacity = '0';
            popup.style.transform = 'translateY(20px)';
            setTimeout(() => {
                popup.style.display = 'none';
            }, 300);
        }

        // Optional: Show popup after 2 seconds
        window.onload = function() {
            setTimeout(() => {
                document.getElementById('promoPopup').classList.add('show');
            }, 2000);
        };