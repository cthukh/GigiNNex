const registerForm = document.getElementById('registerForm');
const loginForm = document.getElementById('loginForm');
const showLogin = document.getElementById('showLogin');
const showRegister = document.getElementById('showRegister');

showLogin.addEventListener('click', (e) => {
    e.preventDefault();
    registerForm.style.display = 'none';
    loginForm.style.display = 'block';
});

showRegister.addEventListener('click', (e) => {
    e.preventDefault();
    loginForm.style.display = 'none';
    registerForm.style.display = 'block';
});

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    console.log('Register:', { username, email, password });
    // enviar datos al backend
});

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    console.log('Login:', { username, password });
    // enviar datos al backend
});

// Alerta al actualizar la pagina
window.addEventListener("beforeunload", function (event) {
    event.preventDefault();
    event.returnValue = "Se borrarán los cambios al actualizar la página.";
});