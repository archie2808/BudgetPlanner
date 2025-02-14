// Use the correct id that matches the form element
document.getElementById("signupForm").addEventListener('submit', function(event) {
    event.preventDefault(); // Stop the default form submission

    // Gather form data into an object
    const formData = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };

    // Send the data as JSON using fetch API to the correct route with prefix "/auth"
    fetch('/auth/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Optionally handle the successful response here
    })
    .catch(error => {
        console.error('Error:', error);
    });
});