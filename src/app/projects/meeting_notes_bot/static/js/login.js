window.addEventListener('load', () => {

    const menuSelectRadio = document.querySelectorAll('input[name="menuSelectRadio"]');

    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    const loginErrorDiv = document.getElementById('loginError');
    const signupErrorDiv = document.getElementById('signupError');

    const loginFormSubmitButton = document.querySelector('#loginForm button[type="submit"]');
    const signupFormSubmitButton = document.querySelector('#signupForm button[type="submit"]');

    menuSelectRadio.forEach((radio) => {
        radio.addEventListener('change', (e) => {
            menuSelectRadio.forEach((radio) => {
                const targetSelector = radio.getAttribute('data-target');
                const targetElement = document.querySelector(targetSelector);
                if (radio.checked) {
                    targetElement.classList.remove('d-none');
                } else {
                    targetElement.classList.add('d-none');
                }
            });
        });
    });

    loginForm.onsubmit = (e) => {

        e.preventDefault();
        loginErrorDiv.classList.add('d-none');
        loginFormSubmitButton.disabled = true;

        apiRequest(
            "auth/login",
            "POST",
            new FormData(loginForm)
        ).then((data) => {
            window.location.href = "/projects/meeting_notes_bot/";
        }).catch((error) => {
            loginErrorDiv.textContent = error.message;
            loginErrorDiv.classList.remove('d-none');
            loginFormSubmitButton.disabled = false;
        });

    };

    signupForm.onsubmit = (e) => {

        e.preventDefault();

        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('signupConfirmPassword').value;

        if (password !== confirmPassword) {
            signupErrorDiv.textContent = 'Passwords do not match.';
            signupErrorDiv.classList.remove('d-none');
            return;
        }

        signupErrorDiv.classList.add('d-none');
        signupFormSubmitButton.disabled = true;

        apiRequest(
            "auth/signup",
            "POST",
            new FormData(signupForm)
        ).then((data) => {
            window.location.href = "/projects/meeting_notes_bot/";
        }).catch((error) => {
            signupErrorDiv.textContent = error.message;
            signupErrorDiv.classList.remove('d-none');
            signupFormSubmitButton.disabled = false;
        });

    };

});