const form = document.querySelector('#login-form');
const rememberMeCheckbox = form.querySelector('#remember-me');
const submitButton = form.querySelector('button[type="submit"]');

submitButton.addEventListener('click', () => {
  if (!rememberMeCheckbox.checked) {
    document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  }
});
