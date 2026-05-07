// Final Frontier - Main Application

let authToken = null;
let currentUser = null;
const API_URL = 'http://localhost:8000/api/v1';

function showPage(pageName) {
    if (!authToken && pageName !== 'login') {
        alert('Please login first');
        return;
    }

    document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
    document.getElementById(pageName).classList.remove('hidden');
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password})
        });

        if (!response.ok) throw new Error('Login failed');

        const data = await response.json();
        authToken = data.access_token;
        currentUser = email;

        document.getElementById('auth-section').classList.add('hidden');
        showPage('dashboard');
        alert('Login successful!');
    } catch (error) {
        alert('Login error: ' + error.message);
    }
}

async function register() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password, full_name: email.split('@')[0]})
        });

        if (!response.ok) throw new Error('Registration failed');

        alert('Registration successful! Now please login.');
    } catch (error) {
        alert('Registration error: ' + error.message);
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    document.getElementById('auth-section').classList.remove('hidden');
    document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
    alert('Logged out');
}

// Page navigation
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('dashboard').classList.remove('hidden');
    document.getElementById('chat').classList.add('hidden');
    document.getElementById('ml').classList.add('hidden');
    document.getElementById('upload').classList.add('hidden');
});
