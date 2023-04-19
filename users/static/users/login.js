// When the login button is clicked, this function will be called
function handleLogin() {
  // Get the email and password input values
  const email = document.getElementById("id_username").value;
  const password = document.getElementById("id_password").value;
  
  // Get the "remember me" checkbox value
  const rememberMe = document.getElementById("id_remember_me").checked;

  // Make an AJAX request to your server to authenticate the user
  fetch('/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      username: email,
      password: password,
      remember_me: rememberMe
    })
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response from the server here
    console.log(data);
    alert('Logged in successfully!');
  })
  .catch(error => {
    console.error(error);
    alert('Error logging in. Please try again.');
  });
}

// Attach an event listener to the login button
const loginButton = document.querySelector('.btn-dark');
loginButton.addEventListener('click', handleLogin);

// Get the value of a cookie by its name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Add an event listener to the "register here" link
const registerLink = document.querySelector('a[href="#!"]');
registerLink.addEventListener('click', event => {
  event.preventDefault();
  // Redirect the user to the registration page
  window.location.href = '/register/';
});


