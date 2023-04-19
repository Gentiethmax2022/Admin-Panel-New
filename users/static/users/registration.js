// Wait for the page to load before binding event listeners
window.addEventListener('load', function() {
  
  // Get the form and input elements
  const form = document.querySelector('form');
  const emailInput = document.getElementById('email');
  const dobInput = document.getElementById('date_of_birth');
  const passwordInput = document.getElementById('password');
  const password2Input = document.getElementById('password2');
  
  // Add an event listener for the form submit event
  form.addEventListener('submit', function(event) {
    
    // Check if the email input is empty
    if (emailInput.value.trim() === '') {
      event.preventDefault();
      alert('Please enter your email address');
      emailInput.focus();
      return;
    }
    
    // Check if the date of birth input is empty
    if (dobInput.value.trim() === '') {
      event.preventDefault();
      alert('Please enter your date of birth');
      dobInput.focus();
      return;
    }
    
    // Check if the password input is empty
    if (passwordInput.value.trim() === '') {
      event.preventDefault();
      alert('Please enter a password');
      passwordInput.focus();
      return;
    }
    
    // Check if the password confirmation input is empty
    if (password2Input.value.trim() === '') {
      event.preventDefault();
      alert('Please confirm your password');
      password2Input.focus();
      return;
    }
    
    // Check if the passwords match
    if (passwordInput.value !== password2Input.value) {
      event.preventDefault();
      alert('Passwords do not match');
      password2Input.focus();
      return;
    }
  });
});


