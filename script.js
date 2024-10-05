document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    // Показати форму входу
    function showLogin() {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    }

    // Показати форму реєстрації
    function showRegister() {
        registerForm.style.display = 'block';
        loginForm.style.display = 'none';
    }

    // Симуляція входу
    async function login(event) {
        event.preventDefault();
        const formData = new FormData(loginForm);
        const response = await fetch('/login', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            alert("Успішний вхід!");
        } else {
            alert("Помилка входу!");
        }
    }

    // Симуляція реєстрації
    async function register(event) {
        event.preventDefault();
        const formData = new FormData(registerForm);
        const response = await fetch('/register', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            alert("Успішна реєстрація!");
        } else {
            alert("Помилка реєстрації!");
        }
    }

    window.showLogin = showLogin;
    window.showRegister = showRegister;
    window.login = login;
    window.register = register;
});
