from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json
import ast

app = Flask(__name__)
CORS(app, 
     resources={r"/*": {
         "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
         "supports_credentials": True
     }})

# Configuración
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Cambia esto en producción
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'autism_learning.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False  # Para desarrollo local
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

db = SQLAlchemy(app)

# Crear carpeta de subida si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Template HTML para la página de inicio
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sistema de Aprendizaje</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Poppins', sans-serif;
        }
        .center-container {
            background: rgba(255,255,255,0.85);
            border-radius: 30px;
            box-shadow: 0 12px 48px 0 rgba(0,0,0,0.18);
            padding: 48px 36px 36px 36px;
            max-width: 420px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            backdrop-filter: blur(8px);
            border: 1.5px solid #e0e0e0;
            animation: popIn 0.8s cubic-bezier(.68,-0.55,.27,1.55);
        }
        @keyframes popIn {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
        h1 {
            color: #222;
            font-size: 2.2em;
            margin-bottom: 24px;
            font-weight: 700;
            text-align: center;
            letter-spacing: 1px;
            text-shadow: 0 2px 8px #b2fefa44;
        }
        .form-group {
            width: 100%;
            margin-bottom: 18px;
            position: relative;
        }
        .form-group input {
            width: 100%;
            padding: 12px 15px 12px 44px;
            background-color: #f0f4f8;
            border: 1.5px solid #e0e0e0;
            border-radius: 12px;
            font-size: 1em;
            transition: border 0.2s, box-shadow 0.2s;
            box-shadow: 0 2px 8px #b2fefa22;
        }
        .form-group input:focus {
            border: 1.5px solid #0091FF;
            outline: none;
            box-shadow: 0 4px 16px #0091ff33;
        }
        .form-group .input-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2em;
            color: #0091FF;
            opacity: 0.7;
        }
        .btn {
            display: inline-block;
            padding: 14px 0;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: 700;
            border: none;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(.68,-0.55,.27,1.55);
            text-transform: uppercase;
            box-shadow: 0 2px 12px #0091ff33;
            outline: none;
            width: 100%;
            margin-top: 8px;
            background: linear-gradient(90deg, #0091FF 60%, #00C6FB 100%);
            color: #fff;
            letter-spacing: 1px;
        }
        .btn:hover, .btn:focus {
            background: linear-gradient(90deg, #00C6FB 60%, #0091FF 100%);
            box-shadow: 0 6px 24px #0091ff44;
            transform: translateY(-2px) scale(1.03);
        }
        .btn-secondary {
            background: #fff;
            color: #0091FF;
            border: 2px solid #0091FF;
            margin-top: 18px;
            transition: background 0.2s, color 0.2s;
        }
        .btn-secondary:hover, .btn-secondary:focus {
            background: #e3f2fd;
            color: #007acc;
        }
        .auth-info {
            margin-top: 28px;
            text-align: center;
            color: #222;
        }
        .auth-info h2 {
            font-size: 1.1em;
            margin-bottom: 6px;
            font-weight: 700;
        }
        .auth-info p {
            font-size: 1em;
            margin-bottom: 10px;
        }
        .error-message, .success-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            display: none;
            text-align: center;
            width: 100%;
        }
        .error-message {
            color: #e74c3c;
            background: #ffd7d7;
        }
        .success-message {
            color: #27ae60;
            background: #d4ffda;
        }
    </style>
</head>
<body>
    <div class="center-container">
        <!-- Formulario de Login -->
        <div class="auth-form" id="loginForm">
            <h1>Iniciar Sesión</h1>
            <div class="error-message" id="loginError"></div>
            <div class="success-message" id="loginSuccess"></div>
            <form onsubmit="handleLogin(event)">
                <div class="form-group">
                    <span class="input-icon">📧</span>
                    <input type="email" name="email" required placeholder="Correo Electrónico">
                </div>
                <div class="form-group">
                    <span class="input-icon">🔒</span>
                    <input type="password" name="password" required placeholder="Contraseña">
                </div>
                <div style="width:100%;display:flex;justify-content:center;">
                  <button type="submit" class="btn" style="width: 70%; max-width: 220px;">Entrar</button>
                </div>
            </form>
        </div>
        <!-- Información adicional -->
        <div class="auth-info">
            <h2>¿Aún no tienes una cuenta?</h2>
            <p>Regístrate para que puedas iniciar sesión</p>
            <a href="#" class="switch-form btn btn-secondary" style="width: 70%; max-width: 220px;" onclick="toggleForms()">Registrarse</a>
        </div>
        <!-- Formulario de Registro -->
        <div class="auth-form" id="registerForm" style="display: none;">
            <h1>Registro</h1>
            <div class="error-message" id="registerError"></div>
            <div class="success-message" id="registerSuccess"></div>
            <form onsubmit="handleRegister(event)">
                <div class="form-group">
                    <input type="text" name="name" required placeholder="Nombre Completo">
                </div>
                <div class="form-group">
                    <input type="email" name="email" required placeholder="Correo Electrónico">
                </div>
                <div class="form-group">
                    <input type="password" name="password" required placeholder="Contraseña">
                </div>
                <div style="width:100%;display:flex;justify-content:center;">
                  <button type="submit" class="btn" style="width: 70%; max-width: 220px;">Registrarse</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        let isLoginForm = true;

        function toggleForms() {
            const loginForm = document.getElementById('loginForm');
            const registerForm = document.getElementById('registerForm');
            const authInfo = document.querySelector('.auth-info');

            if (isLoginForm) {
                loginForm.style.display = 'none';
                registerForm.style.display = 'block';
                authInfo.innerHTML = `
                    <h2>¿Ya tienes una cuenta?</h2>
                    <p>Inicia sesión para continuar aprendiendo</p>
                    <a href="#" class="switch-form btn btn-secondary" style="width: 70%; max-width: 220px;" onclick="toggleForms()">Iniciar Sesión</a>
                `;
            } else {
                loginForm.style.display = 'block';
                registerForm.style.display = 'none';
                authInfo.innerHTML = `
                    <h2>¿Aún no tienes una cuenta?</h2>
                    <p>Regístrate para que puedas iniciar sesión</p>
                    <a href="#" class="switch-form btn btn-secondary" onclick="toggleForms()">Registrarse</a>
                `;
            }
            isLoginForm = !isLoginForm;
        }

        async function handleLogin(event) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    document.getElementById('loginSuccess').style.display = 'block';
                    document.getElementById('loginSuccess').textContent = '¡Inicio de sesión exitoso!';
                    window.location.href = '/dashboard';
                } else {
                    const error = await response.json();
                    document.getElementById('loginError').style.display = 'block';
                    document.getElementById('loginError').textContent = error.error || 'Error al iniciar sesión';
                }
            } catch (error) {
                document.getElementById('loginError').style.display = 'block';
                document.getElementById('loginError').textContent = 'Error de conexión';
            }
        }

        async function handleRegister(event) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    document.getElementById('registerSuccess').style.display = 'block';
                    document.getElementById('registerSuccess').textContent = '¡Registro exitoso! Redirigiendo...';
                    setTimeout(() => {
                        toggleForms();
                    }, 2000);
                } else {
                    const error = await response.json();
                    document.getElementById('registerError').style.display = 'block';
                    document.getElementById('registerError').textContent = error.error || 'Error al registrarse';
                }
            } catch (error) {
                document.getElementById('registerError').style.display = 'block';
                document.getElementById('registerError').textContent = 'Error de conexión';
            }
        }
    </script>
</body>
</html>
"""

# Template para el Dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Sistema de Aprendizaje</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #f0f4f8;
            color: #333;
            font-family: 'Poppins', sans-serif;
            margin: 0;
            min-height: 100vh;
        }
        .dashboard-container {
            display: flex;
            min-height: 100vh;
        }
        .sidebar {
            width: 260px;
            background: #fff;
            box-shadow: 2px 0 16px #0001;
            padding: 32px 20px 20px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            border-radius: 0 30px 30px 0;
            min-height: 100vh;
            flex-shrink: 0; /* Evita que el sidebar se encoja */
            transition: width 0.3s ease; /* Transición suave para responsive */
        }
        .profile-section {
            text-align: center;
            margin-bottom: 30px;
        }
        .profile-photo {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #0091FF;
            margin-bottom: 10px;
        }
        .user-name {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 2px;
        }
        .user-email {
            color: #718096;
            font-size: 0.95em;
        }
        .nav-menu {
            list-style: none;
            padding: 0;
            margin: 30px 0 0 0;
            width: 100%;
        }
        .nav-item {
            margin-bottom: 12px;
        }
        .nav-link {
            display: block;
            padding: 12px 18px;
            color: #2d3748;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 500;
            transition: all 0.3s;
        }
        .nav-link.active, .nav-link:hover {
            background: #E3F2FD;
            color: #0091FF;
        }
        .logout-btn {
            margin-top: auto;
            padding: 12px 20px;
            background: #fff;
            color: #0091FF;
            border: 2px solid #0091FF;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            text-align: center;
            text-decoration: none;
            width: 100%;
        }
        .logout-btn:hover {
            background: #0091FF;
            color: #fff;
        }
        .main-content {
            flex: 1;
            padding: 40px 40px 40px 40px;
            max-width: 1100px;
            margin: 0 auto;
        }
        .section-title {
            font-size: 2em;
            color: #2d3748;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #0091FF;
        }
        .instructions {
            display: flex;
            align-items: center;
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 2px 12px #0091ff11;
            padding: 18px 24px;
            margin-bottom: 24px;
            gap: 18px;
        }
        .instructions img {
            width: 48px;
            height: 48px;
        }
        .study-fields {
            display: flex;
            flex-wrap: wrap;
            gap: 24px;
            justify-content: center;
        }
        .field-card {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 2px 12px #0091ff11;
            padding: 28px 22px;
            min-width: 220px;
            max-width: 260px;
            flex: 1 1 220px;
            text-align: center;
            transition: box-shadow 0.2s, transform 0.2s;
            cursor: pointer;
            border: 2px solid transparent;
        }
        .field-card:hover {
            box-shadow: 0 6px 24px #0091ff22;
            border: 2px solid #0091FF;
            transform: translateY(-6px) scale(1.03);
        }
        .field-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .field-title {
            font-size: 1.2em;
            font-weight: 600;
        }
        .field-description {
            font-size: 1em;
            color: #555;
            margin-bottom: 12px;
        }
        .progress-bar {
            height: 10px;
            background: #E2E8F0;
            border-radius: 8px;
            overflow: hidden;
            margin: 10px 0 6px 0;
        }
        .progress-fill {
            height: 100%;
            background: var(--card-color, #0091FF);
            border-radius: 8px;
            transition: width 0.5s;
        }
        .progress-text {
            display: flex;
            justify-content: space-between;
            color: #718096;
            font-size: 0.9em;
            font-weight: 500;
        }
        .completion-badge {
            position: absolute;
            top: 12px;
            right: 18px;
            background: #fffbe6;
            color: #FFD700;
            border-radius: 50%;
            font-size: 1.3em;
            padding: 4px 8px;
            box-shadow: 0 2px 8px #FFD70033;
        }
        .back-button {
            margin: 18px 0 0 0;
            display: inline-block;
            background: #fff;
            color: #0091FF;
            border: 2px solid #0091FF;
            border-radius: 25px;
            padding: 10px 28px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .back-button:hover {
            background: #0091FF;
            color: #fff;
        }
        /* Sensory Pause & Help Modal */
        .sensory-pause, .help-modal {
            display: none;
            position: fixed;
            z-index: 1001;
            left: 0; top: 0;
            width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
        }
        .sensory-pause.active, .help-modal.active {
            display: flex;
        }
        .sensory-pause > div, .help-content {
            background: #fff;
            border-radius: 20px;
            padding: 40px 32px;
            box-shadow: 0 4px 24px #0002;
            text-align: center;
        }
        .help-content img {
            width: 60px;
            margin-bottom: 10px;
        }
        .help-content button, .sensory-pause button {
            margin-top: 18px;
            padding: 10px 28px;
            border-radius: 25px;
            background: #0091FF;
            color: #fff;
            border: none;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .help-content button:hover, .sensory-pause button:hover {
            background: #007acc;
        }
        /* Responsive */
        @media (max-width: 900px) {
            .dashboard-container {
                flex-direction: column;
            }
            .sidebar {
                width: 100%;
                border-radius: 0 0 30px 30px;
                min-height: unset;
                box-shadow: 0 2px 16px #0001;
                flex-direction: row;
                justify-content: space-between;
                padding: 10px 20px;
            }
            .sidebar .profile-section {
                display: none; /* Ocultar en la barra superior para más espacio */
            }
            .sidebar .nav-menu {
                flex-direction: row;
                margin-top: 0;
                gap: 15px;
            }
            .sidebar .logout-btn {
                margin-top: 0;
            }
            .main-content {
                padding: 24px 8px;
            }
        }
        @media (max-width: 600px) {
            .main-content {
                padding: 12px 2px;
            }
            .field-card {
                min-width: 90vw;
                max-width: 98vw;
            }
        }
        /* Flashcards Mejoradas */
        #flashcardsView {
            margin-top: 24px;
        }
        #flashcardsContainer {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 24px;
        }
        .flashcard {
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 2px 12px #0091ff11;
            padding: 32px 24px;
            max-width: 480px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0 auto;
        }
        .flashcard img {
            width: 120px;
            height: 120px;
            object-fit: contain;
            border-radius: 12px;
            margin-bottom: 18px;
            background: #f0f4f8;
        }
        .flashcard h3 {
            font-size: 1.2em;
            font-weight: 700;
            margin-bottom: 12px;
            text-align: center;
        }
        .flashcard .options {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin-top: 12px;
        }
        .flashcard .options button {
            padding: 14px 22px;
            border-radius: 12px;
            border: none;
            background: #e3f2fd;
            color: #222;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, color 0.2s, transform 0.2s;
            box-shadow: 0 2px 8px #0091ff11;
        }
        .flashcard .options button:hover:not(:disabled) {
            background: #0091FF;
            color: #fff;
            transform: scale(1.05);
        }
        .flashcard .options button.correct {
            background: #27ae60;
            color: #fff;
        }
        .flashcard .options button.incorrect {
            background: #e74c3c;
            color: #fff;
        }
        .flashcard .feedback {
            margin-top: 18px;
            font-size: 1.1em;
            font-weight: 600;
            text-align: center;
            display: none;
        }
        .flashcard .feedback.correct {
            color: #27ae60;
            display: block;
        }
        .flashcard .feedback.incorrect {
            color: #e74c3c;
            display: block;
        }
        .flashcard .listen-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #e3f2fd;
            color: #0091FF;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            padding: 8px 18px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: background 0.2s, color 0.2s;
        }
        .flashcard .listen-btn:hover {
            background: #0091FF;
            color: #fff;
        }
        /* Progreso y navegación */
        #progressIndicator {
            display: flex;
            gap: 8px;
        }
        .progress-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #e0e0e0;
            border: 2px solid #0091FF;
            transition: background 0.2s, border 0.2s;
        }
        .progress-dot.active {
            background: #0091FF;
        }
        .progress-dot.completed {
            background: #27ae60;
            border-color: #27ae60;
        }
        /* Botones navegación */
        #prevButton, #nextButton {
            font-size: 1em;
            font-weight: 600;
            padding: 10px 24px;
            border-radius: 12px;
            min-width: 120px;
        }
        #prevButton:disabled, #nextButton:disabled {
            background: #f0f0f0;
            color: #bbb;
            border: 1.5px solid #e0e0e0;
            cursor: not-allowed;
        }
        .flashcard .options.emotion-options {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            width: 100%;
            max-width: 380px;
            margin: 12px auto 0;
        }
        .emotion-option-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #f0f4f8;
            border: 2px solid transparent;
            border-radius: 16px;
            padding: 12px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            text-align: center;
        }
        
        .emotion-option-card:hover {
            border-color: #0091FF;
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0, 145, 255, 0.15);
        }
        
        .emotion-option-card.correct {
            background: #27ae60;
            color: #fff;
            border-color: #27ae60;
        }
        
        .emotion-option-card.incorrect {
            background: #e74c3c;
            color: #fff;
            border-color: #e74c3c;
        }
        .emotion-option-card img {
            width: 70px;
            height: 70px;
            object-fit: contain;
            margin-bottom: 8px;
        }
        .emotion-option-card span {
            margin-top: 4px;
        }

        /* Completion Message Modal */
        #completionOverlay {
            position: fixed;
            z-index: 1002;
            left: 0; top: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            display: none; /* Initially hidden */
            justify-content: center;
            align-items: center;
        }
        .completion-box {
            background: #fff;
            border-radius: 24px;
            padding: 40px 32px;
            box-shadow: 0 4px 24px #0002;
            text-align: center;
            max-width: 420px;
            animation: popIn 0.5s cubic-bezier(.68,-0.55,.27,1.55);
        }
        .completion-box .confetti {
            font-size: 4em;
            margin-bottom: 10px;
        }
        .completion-box h2 {
            font-size: 1.8em;
            color: #0091FF;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .completion-box p {
            font-size: 1.1em;
            color: #333;
            margin-bottom: 25px;
        }
        .completion-box button {
            margin-top: 18px;
            padding: 12px 32px;
            border-radius: 25px;
            background: #0091FF;
            color: #fff;
            border: none;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .completion-box button:hover {
            background: #007acc;
            transform: translateY(-2px);
        }
    </style>
</head>
<body style="background: linear-gradient(135deg, #e3f0ff 0%, #c3e2ff 100%);">
    <div class="dashboard-container">
        <div class="sidebar">
            <div class="profile-section">
                <img src="{{ current_user.profile_photo }}" alt="Profile Photo" class="profile-photo">
                <h2 class="user-name">{{ current_user.name }}</h2>
                <p class="user-email">{{ current_user.email }}</p>
            </div>
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="/dashboard" class="nav-link active">📊 Dashboard</a>
                </li>
                <li class="nav-item">
                    <a href="/profile" class="nav-link">👤 Mi Perfil</a>
                </li>
                <li class="nav-item">
                    <a href="/progress" class="nav-link">📈 Mi Progreso</a>
                </li>
            </ul>
            <a href="/logout" class="logout-btn">Cerrar Sesión</a>
        </div>
        <div class="main-content" style="background: rgba(255,255,255,0.95); border-radius: 30px; box-shadow: 0 8px 32px #0091ff22;">
            <div class="instructions">
                <img src="https://static.arasaac.org/pictograms/43633/43633_300.png" alt="Instrucciones" style="width:40px;height:40px;border-radius:50%;object-fit:cover;margin-right:16px;vertical-align:middle;">
                <span style="vertical-align:middle;">Escucha la pregunta, mira la imagen y elige la respuesta correcta. Puedes usar el botón de ayuda <b>❓</b> o el botón de pausa sensorial <b>🧘</b> si lo necesitas.</span>
            </div>
            <button id="backButton" class="back-button" onclick="showDashboard()" style="display:none;">← Volver a Campos de Estudio</button>
            <div id="dashboardView">
                <h1 class="section-title">Campo de Estudio</h1>
                <div class="study-fields">
                    {% for field in study_fields %}
                    <div class="field-card" style="--card-color: {{ field.color }}" data-category="{{ field.route }}"
                        onclick="loadFlashcards('{{ field.route }}')">
                        {% if field.completed %}
                        <div class="completion-badge" title="¡Completado!">🌟</div>
                        {% endif %}
                        <div class="field-icon" style="font-size:3em;">{{ field.icon }}</div>
                        <h3 class="field-title">{{ field.name }}</h3>
                        <span class="flashcard-badge" style="display:inline-block;background:#0091FF;color:#fff;font-size:0.9em;font-weight:600;padding:3px 14px;border-radius:12px;margin-bottom:8px;letter-spacing:1px;">Flashcards</span>
                        <p class="field-description">{{ field.description }}</p>
                        <div class="motivation-message" style="margin:8px 0 8px 0;font-size:1em;color:#0091FF;font-weight:600;">
                            <script>var motivaciones = ['¡Tú puedes!', '¡Sigue aprendiendo!', '¡Eres increíble!', '¡Nunca dejes de intentarlo!', '¡Cada día mejoras más!', '¡Aprender es divertido!', '¡Sigue así, lo haces genial!', '¡Eres un campeón!', '¡No te rindas!', '¡Explora y diviértete!'];
document.write(motivaciones[Math.floor(Math.random()*motivaciones.length)]);</script>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {{ field.progress }}%"></div>
                        </div>
                        <div class="progress-text">
                            <span>Progreso</span>
                            <span class="progress-percentage">{{ "%.0f"|format(field.progress) }}%</span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            <!-- Vista de Flashcards -->
            <div id="flashcardsView" style="display:none;">
                <h1 class="section-title" id="categoryTitle"></h1>
                <div id="streakCounter" style="display:none;font-size:1.2em;font-weight:600;margin-bottom:10px;"></div>
                <div id="flashcardsContainer"></div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:24px;">
                    <button id="prevButton" class="btn btn-secondary" onclick="previousCard()" style="min-width:120px;">← Anterior</button>
                    <div id="progressIndicator" style="display:flex;gap:8px;"></div>
                    <button id="nextButton" class="btn btn-primary" onclick="nextCard()" style="min-width:120px;">Siguiente →</button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Completion Message -->
    <div id="completionOverlay">
        <div class="completion-box">
            <div class="confetti">🎉🥳🎊</div>
            <h2>¡Felicitaciones!</h2>
            <p id="finalScoreText"></p>
            <button onclick="showDashboard()">Volver a Campos de Estudio</button>
        </div>
    </div>

    <!-- Sensory Pause y Help Modal fuera del dashboard-container para overlay -->
    <div class="sensory-pause" id="sensoryPause">
        <div>
            <h2>Momento de Pausa</h2>
            <div style="font-size:4em;">🌈✨</div>
            <p style="font-size:1.3em;">Respira profundo y relájate</p>
            <button onclick="hideSensoryPause()">Volver</button>
        </div>
    </div>
    <div class="help-modal" id="helpModal">
        <div class="help-content">
            <img src="https://static.arasaac.org/pictograms/410/410_300.png" alt="Ayuda">
            <h2>¿Cómo usar la tarjeta?</h2>
            <p>Escucha la pregunta, observa la imagen y elige la respuesta correcta. Si necesitas, puedes escuchar la pregunta de nuevo o pedir ayuda a un adulto.</p>
            <button onclick="hideHelp()">Cerrar</button>
        </div>
    </div>
    <button onclick="toggleContrast()" class="back-button" style="position:fixed;top:20px;left:20px;z-index:1100;width:48px;height:48px;border-radius:50%;font-size:1.5em;">🌗</button>
    <button onclick="showHelp()" class="back-button" style="position:fixed;bottom:100px;right:30px;z-index:1100;width:60px;height:60px;border-radius:50%;font-size:2em;">❓</button>
    <button onclick="showSensoryPause()" class="back-button" style="position:fixed;bottom:30px;right:30px;z-index:1100;width:60px;height:60px;border-radius:50%;font-size:2em;">🧘</button>

    <!-- Audio para feedback -->
    <audio id="audio-correct" src="https://freesound.org/data/previews/391/391715_5674468-lq.mp3" preload="auto"></audio>
    <audio id="audio-wrong" src="https://freesound.org/data/previews/171/171493_2112491-lq.mp3" preload="auto"></audio>

    <script>
        let currentCardIndex = 0;
        let currentFlashcards = [];
        let answeredCards = new Map();
        let correctAnswers = 0;
        let currentCategory = '';
        let streak = 0;
        const motivacion = [
            '¡Sigue así, lo estás haciendo genial! 💪',
            '¡No te rindas, cada intento cuenta! 🌟',
            '¡Eres muy inteligente, continúa aprendiendo! 🧠',
            '¡Excelente trabajo, sigue practicando! 👏',
            '¡Vas por buen camino! 🚀',
            '¡Recuerda, equivocarse es aprender! 😊',
            '¡Tú puedes, inténtalo de nuevo! 💡',
            '¡Muy bien, cada vez mejoras más! 🥳',
            '¡Sigue practicando, lo lograrás! 👍',
            '¡Eres un campeón! 🏆'
        ];

        function showDashboard() {
            const dashboardView = document.getElementById('dashboardView');
            const flashcardsView = document.getElementById('flashcardsView');
            const backButton = document.getElementById('backButton');
            const completionOverlay = document.getElementById('completionOverlay');
            if (dashboardView) dashboardView.style.display = 'block';
            if (flashcardsView) flashcardsView.style.display = 'none';
            if (backButton) backButton.style.display = 'none';
            if (completionOverlay) completionOverlay.style.display = 'none';
            // Reset state
            currentCardIndex = 0;
            currentFlashcards = [];
            answeredCards = new Map(); // Limpiar correctamente el set
            correctAnswers = 0;
            streak = 0;
            updateDashboardProgress();
        }

        function showFlashcards() {
            const dashboardView = document.getElementById('dashboardView');
            const flashcardsView = document.getElementById('flashcardsView');
            const backButton = document.getElementById('backButton');
            if (dashboardView) dashboardView.style.display = 'none';
            if (flashcardsView) flashcardsView.style.display = 'block';
            if (backButton) backButton.style.display = 'block';
        }

        function updateProgressDots() {
            const progressIndicator = document.getElementById('progressIndicator');
            progressIndicator.innerHTML = '';
            
            currentFlashcards.forEach((_, index) => {
                const dot = document.createElement('div');
                dot.className = 'progress-dot';
                if (index === currentCardIndex) dot.className += ' active';
                if (answeredCards.has(index)) {
                    dot.className += ' completed';
                }
                progressIndicator.appendChild(dot);
            });
        }

        function updateNavigationButtons() {
            const prevButton = document.getElementById('prevButton');
            const nextButton = document.getElementById('nextButton');
            if (!prevButton || !nextButton) return;

            prevButton.disabled = currentCardIndex === 0;

            const isAnswered = answeredCards.has(currentCardIndex);
            
            if (currentCardIndex === currentFlashcards.length - 1) {
                nextButton.textContent = 'Finalizar';
                // Habilitar el botón "Finalizar" solo si todas las tarjetas han sido respondidas
                nextButton.disabled = answeredCards.size !== currentFlashcards.length;
            } else {
                nextButton.textContent = 'Siguiente →';
                nextButton.disabled = !isAnswered;
            }
        }
        
        function updateStreakCounter() {
            const streakCounter = document.getElementById('streakCounter');
            if (!streakCounter) return;
            if (streak > 0) {
                streakCounter.textContent = `🔥 ${streak}`;
                streakCounter.style.display = 'block';
            } else {
                streakCounter.style.display = 'none';
            }
        }

        function displayCurrentCard() {
            const container = document.getElementById('flashcardsContainer');
            if (!container || !currentFlashcards || currentFlashcards.length === 0) return;
            const card = currentFlashcards[currentCardIndex];
            container.innerHTML = '';

            const flashcardEl = document.createElement('div');
            flashcardEl.className = 'flashcard';

            const imgEl = document.createElement('img');
            imgEl.src = card.image_url;
            imgEl.alt = card.question;
            flashcardEl.appendChild(imgEl);

            const questionEl = document.createElement('h3');
            questionEl.textContent = card.question;
            flashcardEl.appendChild(questionEl);
            
            const listenButton = document.createElement('button');
            listenButton.innerHTML = '🔊 Escuchar';
            listenButton.className = 'listen-btn';
            listenButton.onclick = () => speakText(card.question);
            flashcardEl.appendChild(listenButton);

            const optionsEl = document.createElement('div');
            optionsEl.className = 'options';

            // --- Layout para Emociones y Comunicación ---
            if (currentCategory === 'emociones') {
                optionsEl.classList.add('emotion-options');
                
                const imageMap = {
                    'emociones': {
                    'Feliz': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Smiling%20face%20with%20smiling%20eyes/3D/smiling_face_with_smiling_eyes_3d.png',
                    'Triste': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Frowning%20face/3D/frowning_face_3d.png',
                    'Enojado': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Angry%20face/3D/angry_face_3d.png',
                    'Sorprendido': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Hushed%20face/3D/hushed_face_3d.png'
                    }
                };

                const currentImageMap = imageMap[currentCategory];

                card.options.forEach((option, index) => {
                    const optionCard = document.createElement('button');
                    optionCard.className = 'emotion-option-card';
                    optionCard.type = 'button';
                    optionCard.onclick = () => checkAnswer(index, card.correct_option, card.feedback);
                    
                    const pictoImg = document.createElement('img');
                    pictoImg.src = currentImageMap[option] || '';
                    pictoImg.alt = option;
                    
                    const optionText = document.createElement('span');
                    optionText.textContent = option;
                    
                    optionCard.appendChild(pictoImg);
                    optionCard.appendChild(optionText);
                    optionsEl.appendChild(optionCard);
                });
            } else {
                // Layout estándar para otras categorías
                card.options.forEach((option, index) => {
                    const buttonEl = document.createElement('button');
                    buttonEl.textContent = option;
                    buttonEl.type = 'button';
                    buttonEl.style.background = '#e3f2fd';
                    buttonEl.style.color = '#222';
                    buttonEl.style.fontSize = '1.1em';
                    buttonEl.style.fontWeight = '600';
                    buttonEl.style.padding = '14px 22px';
                    buttonEl.style.borderRadius = '12px';
                    buttonEl.style.border = 'none';
                    buttonEl.style.margin = '6px';
                    buttonEl.style.cursor = 'pointer';
                    buttonEl.style.transition = 'background 0.2s, color 0.2s, transform 0.2s';
                    buttonEl.style.boxShadow = '0 2px 8px #0091ff11';
                    buttonEl.disabled = false;
                    buttonEl.style.pointerEvents = 'auto';
                    buttonEl.onclick = () => checkAnswer(index, card.correct_option, card.feedback);
                    optionsEl.appendChild(buttonEl);
                });
            }
            flashcardEl.appendChild(optionsEl);

            const feedbackEl = document.createElement('div');
            feedbackEl.className = 'feedback';
            flashcardEl.appendChild(feedbackEl);

            container.appendChild(flashcardEl);
            updateProgressDots();
            updateNavigationButtons();
            
            // Si la tarjeta ya fue respondida, mostrar el resultado visual
            if (answeredCards.has(currentCardIndex)) {
                const selectedIndex = answeredCards.get(currentCardIndex);
                showAnswerResult(selectedIndex, card.correct_option, card.feedback, false);
            }
        }
        
        async function loadFlashcards(category) {
            try {
                currentCategory = category;
                const response = await fetch(`/api/flashcards/${category}`);

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`El servidor respondió con un error ${response.status}. Detalles: ${errorText}`);
                }
                
                const responseData = await response.json();

                // Asegurar que las opciones sean un array
                responseData.forEach(card => {
                    if (typeof card.options === 'string') {
                        try {
                            card.options = JSON.parse(card.options);
                        } catch (e) {
                            // Si falla, deja el valor original
                        }
                    }
                });

                if (!Array.isArray(responseData) || responseData.length === 0) {
                    throw new Error('No se encontraron tarjetas para esta categoría o los datos están vacíos.');
                }
                
                currentFlashcards = responseData;
                
                // Reset state
                currentCardIndex = 0;
                answeredCards.clear();
                correctAnswers = 0;
                streak = 0;
                updateStreakCounter();
                
                // Set category title
                const titles = {
                    'emociones': 'Desarrollo Emocional',
                    'conceptos': 'Conceptos Básicos',
                    'entorno': 'Conocimiento del Entorno'
                };
                const categoryTitle = document.getElementById('categoryTitle');
                if (categoryTitle) categoryTitle.textContent = titles[category];
                
                displayCurrentCard();
                showFlashcards();

                // Cargar progreso existente
                await loadExistingProgress(category);
            } catch (error) {
                console.error('Error detallado al cargar flashcards:', error);
                alert(`Error al cargar las tarjetas: ${error.message}`);
            }
        }
        
        function previousCard() {
            if (currentCardIndex > 0) {
                currentCardIndex--;
                displayCurrentCard();
            }
        }

        function nextCard() {
            if (currentCardIndex < currentFlashcards.length - 1) {
                currentCardIndex++;
                displayCurrentCard();
            } else if (answeredCards.size === currentFlashcards.length) {
                const percentage = (correctAnswers / currentFlashcards.length) * 100;
                showCompletionMessage(correctAnswers, percentage);
            }
        }

        async function loadExistingProgress(category) {
            try {
                const response = await fetch('/get-all-progress');
                const progressData = await response.json();
                
                if (progressData[category]) {
                    const progress = progressData[category];
                    // Restaurar el estado de progreso
                    correctAnswers = progress.score;
                    
                    // La restauración visual del estado de cada tarjeta desde el servidor
                    // no es posible con la estructura actual, ya que no se guarda la respuesta
                    // seleccionada para cada tarjeta. Se deja el progreso numérico pero
                    // la sesión de flashcards empieza visualmente desde cero.
                    
                    updateProgressDots();
                    updateNavigationButtons();
                }
            } catch (error) {
                console.error('Error loading progress:', error);
            }
        }

        async function saveProgress(category, score, percentage, completed, answeredCount) {
            try {
                const response = await fetch('/save-progress', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        category: category,
                        score: score,
                        percentage: percentage,
                        completed: completed,
                        answered_cards: answeredCount
                    })
                });

                if (!response.ok) {
                    throw new Error('Error al guardar el progreso');
                }

                const result = await response.json();
                console.log('Progreso guardado:', result);

                // Mostrar mensaje de completado si corresponde
                if (completed) {
                    showCompletionMessage(score, percentage);
                }
            } catch (error) {
                console.error('Error saving progress:', error);
            }
        }

        function updateProgressUI(category, percentage) {
            try {
                const currentCard = document.querySelector(`[data-category="${category}"]`);
                if (!currentCard) return;
                const progressBar = currentCard.querySelector('.progress-fill');
                const progressText = currentCard.querySelector('.progress-percentage');
                if (progressBar) { progressBar.style.width = `${percentage}%`; }
                if (progressText) { progressText.textContent = `${Math.round(percentage)}%`; }
            } catch (e) {
                console.error("Error updating progress UI:", e);
            }
        }

        async function updateDashboardProgress() {
            try {
                const dashboardView = document.getElementById('dashboardView');
                if (!dashboardView || dashboardView.style.display === 'none') return;
                const response = await fetch('/get-all-progress');
                const progressData = await response.json();
                Object.entries(progressData).forEach(([category, data]) => {
                    const card = document.querySelector(`[data-category="${category}"]`);
                    if (!card) return;
                    const progressBar = card.querySelector('.progress-fill');
                    const progressText = card.querySelector('.progress-percentage');
                    if (progressBar) { progressBar.style.width = `${data.percentage}%`; }
                    if (progressText) { progressText.textContent = `${Math.round(data.percentage)}%`; }
                });
            } catch (e) {
                return;
            }
        }

        function showCompletionMessage(score, percentage) {
            const finalScoreText = document.getElementById('finalScoreText');
            if (finalScoreText) {
                finalScoreText.textContent = `¡Has completado la actividad con ${score} de ${currentFlashcards.length} respuestas correctas!`;
            }
            const completionOverlay = document.getElementById('completionOverlay');
            if (completionOverlay) completionOverlay.style.display = 'flex';
        }

        function showAnswerResult(selectedIndex, correctIndex, feedback, showMotivation = false) {
            const isCorrect = selectedIndex === correctIndex;
            const options = document.querySelectorAll('.flashcard .options > *');
            const feedbackElement = document.querySelector('.flashcard .feedback');
            const flashcardEl = document.querySelector('.flashcard');
            
            let feedbackHTML = '';
            if (isCorrect) {
                feedbackHTML = `<span class='big-emoji'>👏😃</span> ¡Correcto! ${feedback}`;
            } else {
                feedbackHTML = `<span class='big-emoji'>😕</span> Incorrecto, intenta de nuevo`;
            }

            if (showMotivation) {
                const mensajeMotivacion = motivacion[Math.floor(Math.random() * motivacion.length)];
                feedbackHTML += `<br><span style='display:block;margin-top:10px;font-size:1em;color:#0091FF;'>${mensajeMotivacion}</span>`;
            }

            feedbackElement.innerHTML = feedbackHTML;

            options.forEach((optionEl, index) => {
                optionEl.style.pointerEvents = 'none';
                optionEl.disabled = true;
                if (index === correctIndex) {
                    optionEl.classList.add('correct');
                }
            });

            if (!isCorrect && selectedIndex >= 0 && options[selectedIndex]) {
                options[selectedIndex].classList.add('incorrect');
            }
            
            feedbackElement.className = `feedback ${isCorrect ? 'correct' : 'incorrect'}`;
            feedbackElement.style.display = 'block';

            if (flashcardEl && showMotivation) {
                if (isCorrect) flashcardEl.classList.add('bounce');
                else flashcardEl.classList.add('shake');
                
                setTimeout(() => {
                    flashcardEl.classList.remove('bounce', 'shake');
                }, 1000);
            }
        }

        function checkAnswer(selectedIndex, correctIndex, feedback) {
            if (answeredCards.has(currentCardIndex)) {
                return;
            }

            // Guardar la respuesta
            answeredCards.set(currentCardIndex, selectedIndex);

            const isCorrect = selectedIndex === correctIndex;
            
            if (isCorrect) {
                correctAnswers++;
                streak++;
                playSound('correct');
            } else {
                streak = 0;
                playSound('wrong');
            }
            
            // Mostrar feedback visual
            showAnswerResult(selectedIndex, correctIndex, feedback, true);
            
            updateStreakCounter();

            const totalCards = currentFlashcards.length;
            const completed = answeredCards.size === totalCards;
            
            // El porcentaje ahora se basa en la puntuación
            const scorePercentage = totalCards > 0 ? (correctAnswers / totalCards) * 100 : 0;
            
            saveProgress(
                currentCategory,
                correctAnswers,
                scorePercentage,
                completed,
                answeredCards.size
            );

            // Actualizar la UI del dashboard en tiempo real
            updateProgressUI(currentCategory, scorePercentage);
            
            updateProgressDots();
            updateNavigationButtons();
        }

        function returnToDashboard() {
            window.location.href = '/dashboard';
        }

        function toggleContrast() {
            document.body.classList.toggle('high-contrast');
        }
        function showHelp() {
            document.getElementById('helpModal').classList.add('active');
        }
        function hideHelp() {
            document.getElementById('helpModal').classList.remove('active');
        }
        function showSensoryPause() {
            document.getElementById('sensoryPause').classList.add('active');
        }
        function hideSensoryPause() {
            document.getElementById('sensoryPause').classList.remove('active');
        }
        function playSound(type) {
            try {
                if (type === 'correct') {
                    const audio = document.getElementById('audio-correct');
                    if(audio) audio.play();
            } else {
                    const audio = document.getElementById('audio-wrong');
                    if(audio) audio.play();
                }
            } catch (e) {
                console.error("No se pudo reproducir el sonido:", e);
            }
        }
        function speakText(text) {
            if ('speechSynthesis' in window) {
                const utter = new SpeechSynthesisUtterance(text);
                utter.lang = 'es-ES';
                window.speechSynthesis.speak(utter);
            }
        }
        function repeatQuestion() {
            if(currentFlashcards[currentCardIndex]) {
                speakText(currentFlashcards[currentCardIndex].question);
            }
        }

        window.onerror = function(message, source, lineno, colno, error) {
            console.error('Error global capturado:', message, source, lineno, colno, error);
            return true; // Evita el alert
        };
    </script>
</body>
</html>
"""

# Template para la página de perfil
PROFILE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mi Perfil - Sistema de Aprendizaje</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Estilos base reutilizados y mejorados */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            min-height: 100vh;
            background: #f0f4f8; /* Un fondo más suave */
            display: flex;
        }

        .sidebar {
            width: 260px;
            background: white;
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            border-right: 1px solid #e9eef2;
            position: fixed;
            height: 100vh;
            box-shadow: 2px 0 16px #0001;
        }

        .profile-section {
            text-align: center;
            margin-bottom: 25px;
        }

        .profile-photo {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin-bottom: 12px;
            object-fit: cover;
            border: 4px solid #0091FF;
        }

        .user-name {
            font-size: 1.3em;
            color: #2d3748;
            font-weight: 600;
        }

        .user-email {
            color: #718096;
            font-size: 0.9em;
        }

        .nav-menu {
            list-style: none;
            margin-top: 20px;
        }

        .nav-item {
            margin-bottom: 10px;
        }

        .nav-link {
            display: flex;
            align-items: center;
            padding: 12px 18px;
            color: #2d3748;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .nav-link:hover {
            background: #e3f2fd;
            color: #0091FF;
        }

        .nav-link.active {
            background: #0091FF;
            color: white;
        }

        .logout-btn {
            margin-top: auto;
            padding: 12px 20px;
            background: #fff;
            color: #e53e3e;
            border: 2px solid #e53e3e;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
            text-align: center;
        }

        .logout-btn:hover {
            background: #e53e3e;
            color: white;
        }

        .main-content {
            flex: 1;
            margin-left: 260px;
            padding: 40px;
        }

        .profile-container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        }

        .section-title {
            font-size: 2em;
            color: #2d3748;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #0091FF;
        }

        .profile-form-layout {
            display: flex;
            gap: 40px;
            align-items: flex-start;
        }
        
        .avatar-preview-section {
            flex-shrink: 0;
            text-align: center;
        }

        .avatar-upload-container {
            position: relative;
            width: 150px;
            height: 150px;
            margin: 0 auto;
        }

        .upload-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 50%;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s ease;
            font-weight: 600;
        }
        
        .avatar-upload-container:hover .upload-overlay {
            opacity: 1;
        }

        .avatar-preview-section label {
            display: block;
            margin-bottom: 15px;
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }

        #current-avatar-preview {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid #0091FF;
            box-shadow: 0 4px 12px rgba(0, 145, 255, 0.2);
        }

        .form-fields-section {
            flex-grow: 1;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #2d3748;
            font-weight: 500;
        }

        .form-group input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e1e1;
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s ease;
        }

        .form-group input:focus {
            outline: none;
            border-color: #0091FF;
            box-shadow: 0 0 0 3px rgba(0, 145, 255, 0.1);
        }

        .avatar-selection-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e9eef2;
        }

        .avatar-selection-section > label {
            display: block;
            margin-bottom: 15px;
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        .avatar-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(75px, 1fr));
            gap: 1rem;
        }

        .avatar-option {
            cursor: pointer;
            border-radius: 50%;
            padding: 3px;
            border: 3px solid transparent;
            transition: all 0.2s ease;
            position: relative;
        }

        .avatar-option:hover {
            transform: scale(1.08);
            border-color: #b3dfff;
        }

        .avatar-option.selected {
            border-color: #0091FF;
        }

        .avatar-option img {
            width: 100%;
            height: auto;
            border-radius: 50%;
            display: block;
        }

        .save-btn {
            padding: 14px 30px;
            background: #0091FF;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 30px;
        }

        .save-btn:hover {
            background: #007acc;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 145, 255, 0.3);
        }

        @media (max-width: 900px) {
            .main-content {
                margin-left: 0;
            }
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
                border-right: none;
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
            }
            .profile-section {
                display: flex;
                align-items: center;
                gap: 15px;
                border: none;
            }
            .nav-menu {
                display: flex;
                gap: 10px;
                margin-top: 0;
            }
            .logout-btn {
                margin-top: 0;
            }
            .profile-form-layout {
                flex-direction: column;
                align-items: center;
                gap: 25px;
            }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="profile-section">
            <img src="{{ current_user.profile_photo }}" alt="Profile Photo" class="profile-photo">
            <div>
            <h2 class="user-name">{{ current_user.name }}</h2>
            <p class="user-email">{{ current_user.email }}</p>
            </div>
        </div>
        <ul class="nav-menu">
            <li class="nav-item"><a href="/dashboard" class="nav-link">📊 Dashboard</a></li>
            <li class="nav-item"><a href="/profile" class="nav-link active">👤 Mi Perfil</a></li>
            <li class="nav-item"><a href="/progress" class="nav-link">📈 Mi Progreso</a></li>
        </ul>
        <a href="/logout" class="logout-btn">Cerrar Sesión</a>
    </div>

    <div class="main-content">
        <div class="profile-container">
            <h1 class="section-title">Editar Perfil</h1>
            <form action="/update-profile" method="POST" enctype="multipart/form-data">
                <div class="profile-form-layout">
                    <div class="avatar-preview-section">
                        <label>Tu Avatar</label>
                        <div class="avatar-upload-container">
                            <img src="{{ current_user.profile_photo }}" alt="Avatar actual" id="current-avatar-preview">
                            <label for="avatar-upload-input" class="upload-overlay">
                                <span>Cambiar</span>
                            </label>
                            <input type="file" id="avatar-upload-input" name="avatar_file" accept="image/*" style="display:none;">
                        </div>
                        <input type="hidden" id="profile_photo" name="profile_photo" value="{{ current_user.profile_photo }}">
                    </div>

                    <div class="form-fields-section">
                <div class="form-group">
                    <label for="name">Nombre Completo</label>
                    <input type="text" id="name" name="name" value="{{ current_user.name }}" required>
                </div>
                <div class="form-group">
                    <label for="email">Correo Electrónico</label>
                    <input type="email" id="email" name="email" value="{{ current_user.email }}" required>
                </div>
                <div class="form-group">
                            <label for="password">Nueva Contraseña</label>
                            <input type="password" id="password" name="password" placeholder="Dejar en blanco para no cambiar">
                        </div>
                        </div>
                        </div>

                <div class="avatar-selection-section">
                    <label>O elige uno nuevo:</label>
                    <div class="avatar-grid">
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/adventurer/svg?seed=Felix')"><img src="https://api.dicebear.com/8.x/adventurer/svg?seed=Felix" alt="Avatar 1"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/adventurer/svg?seed=Mimi')"><img src="https://api.dicebear.com/8.x/adventurer/svg?seed=Mimi" alt="Avatar 2"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/big-smile/svg?seed=Salem')"><img src="https://api.dicebear.com/8.x/big-smile/svg?seed=Salem" alt="Avatar 3"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/big-smile/svg?seed=Rocky')"><img src="https://api.dicebear.com/8.x/big-smile/svg?seed=Rocky" alt="Avatar 4"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/bottts-neutral/svg?seed=bot1')"><img src="https://api.dicebear.com/8.x/bottts-neutral/svg?seed=bot1" alt="Avatar 5"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/bottts-neutral/svg?seed=bot2')"><img src="https://api.dicebear.com/8.x/bottts-neutral/svg?seed=bot2" alt="Avatar 6"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/micah/svg?seed=micah1')"><img src="https://api.dicebear.com/8.x/micah/svg?seed=micah1" alt="Avatar 7"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/micah/svg?seed=micah2')"><img src="https://api.dicebear.com/8.x/micah/svg?seed=micah2" alt="Avatar 8"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/open-peeps/svg?seed=peep1')"><img src="https://api.dicebear.com/8.x/open-peeps/svg?seed=peep1" alt="Avatar 9"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/open-peeps/svg?seed=peep2')"><img src="https://api.dicebear.com/8.x/open-peeps/svg?seed=peep2" alt="Avatar 10"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/fun-emoji/svg?seed=emoji1')"><img src="https://api.dicebear.com/8.x/fun-emoji/svg?seed=emoji1" alt="Avatar 11"></div>
                        <div class="avatar-option" onclick="selectAvatar('https://api.dicebear.com/8.x/fun-emoji/svg?seed=emoji2')"><img src="https://api.dicebear.com/8.x/fun-emoji/svg?seed=emoji2" alt="Avatar 12"></div>
                        </div>
                        </div>
                <button type="submit" class="save-btn">Guardar Cambios</button>
            </form>
        </div>
    </div>

    <script>
        function selectAvatar(url) {
            // Update hidden input value
            document.getElementById('profile_photo').value = url;
            
            // Update visual selection in the grid
            document.querySelectorAll('.avatar-option').forEach(option => {
                option.classList.toggle('selected', option.querySelector('img').src === url);
            });

            // Update the main preview image on the page
            document.getElementById('current-avatar-preview').src = url;

            // Update the sidebar profile photo preview
            document.querySelector('.sidebar .profile-photo').src = url;
            
            // Clear the file input if a pre-defined avatar is selected
            const fileInput = document.getElementById('avatar-upload-input');
            fileInput.value = '';
        }

        document.getElementById('avatar-upload-input').addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('current-avatar-preview');
                    const sidebarPreview = document.querySelector('.sidebar .profile-photo');
                    preview.src = e.target.result;
                    sidebarPreview.src = e.target.result;
                    
                    // Clear pre-defined avatar selection
                    document.querySelectorAll('.avatar-option').forEach(option => {
                        option.classList.remove('selected');
                    });
                }
                reader.readAsDataURL(file);
            }
        });

        // Set initial selection when the page loads
        window.onload = function() {
            const currentUrl = document.getElementById('profile_photo').value;
            if (currentUrl) {
                document.querySelectorAll('.avatar-option').forEach(option => {
                if (option.querySelector('img').src === currentUrl) {
                    option.classList.add('selected');
                }
            });
            }
        }
    </script>
</body>
</html>
"""

# Template para la página de progreso
PROGRESS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mi Progreso - Sistema de Aprendizaje</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Reutilizar los estilos base */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            min-height: 100vh;
            background: #E3F2FD;
            display: flex;
        }

        .sidebar {
            width: 280px;
            background: white;
            padding: 30px;
            display: flex;
            flex-direction: column;
            border-right: 1px solid #e1e1e1;
            position: fixed;
            height: 100vh;
        }

        .profile-section {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            border-bottom: 1px solid #e1e1e1;
        }

        .profile-photo {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin-bottom: 15px;
            object-fit: cover;
            border: 3px solid #0091FF;
        }

        .user-name {
            font-size: 1.5em;
            color: #2d3748;
            margin-bottom: 5px;
        }

        .user-email {
            color: #718096;
            font-size: 0.9em;
        }

        .nav-menu {
            list-style: none;
            margin-top: 20px;
        }

        .nav-item {
            margin-bottom: 15px;
        }

        .nav-link {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            color: #2d3748;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        .nav-link:hover {
            background: #E3F2FD;
            color: #0091FF;
        }

        .nav-link.active {
            background: #0091FF;
            color: white;
        }

        .main-content {
            flex: 1;
            margin-left: 280px;
            padding: 30px;
        }

        .section-title {
            font-size: 2em;
            color: #2d3748;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #0091FF;
        }

        .progress-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }

        .progress-card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .progress-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }

        .progress-icon {
            font-size: 2em;
            margin-right: 15px;
            color: var(--card-color);
        }

        .progress-title {
            font-size: 1.3em;
            color: #2d3748;
            font-weight: 600;
        }

        .progress-stats {
            display: grid;
            gap: 15px;
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: #f7fafc;
            border-radius: 10px;
        }

        .stat-label {
            color: #718096;
            font-weight: 500;
        }

        .stat-value {
            color: #2d3748;
            font-weight: 600;
        }

        .progress-bar {
            height: 15px;
            background: #E2E8F0;
            border-radius: 8px;
            overflow: hidden;
            margin: 15px 0;
        }

        .progress-fill {
            height: 100%;
            background: var(--card-color);
            border-radius: 8px;
            transition: width 0.5s ease;
        }

        .progress-text {
            display: flex;
            justify-content: space-between;
            color: #718096;
            font-size: 0.9em;
            font-weight: 500;
        }

        .logout-btn {
            margin-top: auto;
            padding: 12px 20px;
            background: #e53e3e;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            text-align: center;
        }

        .logout-btn:hover {
            background: #c53030;
        }

        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
                border-right: none;
                border-bottom: 1px solid #e1e1e1;
            }

            .main-content {
                margin-left: 0;
            }

            .progress-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="profile-section">
            <img src="{{ current_user.profile_photo }}" alt="Profile Photo" class="profile-photo">
            <h2 class="user-name">{{ current_user.name }}</h2>
            <p class="user-email">{{ current_user.email }}</p>
        </div>
        <ul class="nav-menu">
            <li class="nav-item">
                <a href="/dashboard" class="nav-link">
                    📊 Dashboard
                </a>
            </li>
            <li class="nav-item">
                <a href="/profile" class="nav-link">
                    👤 Mi Perfil
                </a>
            </li>
            <li class="nav-item">
                <a href="/progress" class="nav-link active">
                    📈 Mi Progreso
                </a>
            </li>
        </ul>
        <a href="/logout" class="btn btn-secondary logout-btn">Cerrar Sesión</a>
    </div>

    <div class="main-content">
        <h1 class="section-title">Mi Progreso</h1>
        <div class="progress-grid">
            {% for field in progress_data %}
            <div class="progress-card" style="--card-color: {{ field.color }}">
                <div class="progress-header">
                    <div class="progress-icon">{{ field.icon }}</div>
                    <h3 class="progress-title">{{ field.name }}</h3>
                </div>
                <div class="progress-stats">
                    <div class="stat-item">
                        <span class="stat-label">Tarjetas Completadas</span>
                        <span class="stat-value">{{ field.completed_cards }}/{{ field.total_cards }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Mejor Puntuación</span>
                        <span class="stat-value">{{ field.best_score }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Última Actividad</span>
                        <span class="stat-value">{{ field.last_activity }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Última Puntuación</span>
                        <span class="stat-value">{{ field.best_score }}/{{ field.total_cards }}</span>
                    </div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ field.progress }}%"></div>
                </div>
                <div class="progress-text">
                    <span>Progreso Total</span>
                    <span class="progress-percentage">{{ "%.0f"|format(field.progress) }}%</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# Modelos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    profile_photo = db.Column(db.String(500), default='https://api.dicebear.com/8.x/adventurer/svg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Float, default=0.0)
    completed_cards = db.Column(db.Integer, default=0)
    total_cards = db.Column(db.Integer, default=3)
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, category, score=0, percentage=0.0, completed_cards=0, completed=False):
        self.user_id = user_id
        self.category = category
        self.score = score
        self.percentage = percentage
        self.completed_cards = completed_cards
        self.completed = completed
        self.updated_at = datetime.utcnow()

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500))
    options = db.Column(db.String(1000), nullable=False)  # JSON string of options
    correct_option = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas de autenticación
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['name', 'email', 'password']):
            return jsonify({'error': 'Faltan datos requeridos'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'El correo electrónico ya está registrado'}), 400
        
        new_user = User(
            name=data['name'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template_string(HTML_TEMPLATE)
        
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()

        if not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Faltan datos requeridos'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        if not user.check_password(data['password']):
            return jsonify({'error': 'Contraseña incorrecta'}), 401
            
        login_user(user)
        return jsonify({'message': 'Login exitoso', 'redirect': url_for('dashboard')}), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/save-progress', methods=['POST'])
@login_required
def save_progress():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['category', 'score', 'percentage']):
            return jsonify({'error': 'Faltan datos requeridos'}), 400

        # Buscar progreso existente
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            category=data['category']
        ).first()

        if not progress:
            # Crear nuevo registro si no existe
            progress = UserProgress(
                user_id=current_user.id,
                category=data['category']
            )
            db.session.add(progress)

        # Actualizar el progreso con la puntuación del último intento
        progress.score = int(data['score'])
        progress.percentage = float(data['percentage'])
        progress.completed_cards = data.get('answered_cards', progress.completed_cards)
        progress.completed = data.get('completed', False)
        progress.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'message': 'Progreso guardado exitosamente',
            'progress': {
                'score': progress.score,
                'percentage': progress.percentage,
                'completed_cards': progress.completed_cards,
                'completed': progress.completed
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error saving progress: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get-progress/<category>')
@login_required
def get_progress(category):
    try:
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            category=category
        ).order_by(UserProgress.updated_at.desc()).first()
        
        if progress:
            return jsonify({
                'score': progress.score,
                'percentage': progress.percentage,
                'completed': progress.completed
            })
        return jsonify({
            'score': 0,
            'percentage': 0,
            'completed': False
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/dashboard')
@login_required
def dashboard():
    categories = {
        'emociones': {
            'name': 'Desarrollo Emocional',
            'icon': '😊',
            'color': '#FF9800',
            'description': 'Aprende sobre emociones y expresiones faciales'
        },
        'conceptos': {
            'name': 'Conceptos Básicos',
            'icon': '📚',
            'color': '#4CAF50',
            'description': 'Aprende formas, colores y números'
        },
        'entorno': {
            'name': 'Conocimiento del Entorno',
            'icon': '🌍',
            'color': '#2196F3',
            'description': 'Aprende sobre animales, clima y naturaleza'
        },
        'vida_diaria': {
            'name': 'Vida Diaria',
            'icon': '🏠',
            'color': '#8BC34A',
            'description': 'Aprende rutinas y actividades cotidianas'
        },
        'comunicacion': {
            'name': 'Comunicación',
            'icon': '🗣️',
            'color': '#FFB300',
            'description': 'Mejora tus habilidades para comunicarte'
        }
    }
    
    study_fields = []
    for key, category in categories.items():
        # Obtener el progreso más reciente
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            category=key
        ).first()
        
        study_fields.append({
            'name': category['name'],
            'route': key,
            'icon': category['icon'],
            'color': category['color'],
            'description': category['description'],
            'progress': progress.percentage if progress else 0,
            'completed_cards': progress.completed_cards if progress else 0,
            'total_cards': 3,  # Total de tarjetas por categoría
            'completed': progress.completed if progress else False
        })

    return render_template_string(
        DASHBOARD_TEMPLATE,
        study_fields=study_fields,
        current_user=current_user
    )

@app.route('/profile')
@login_required
def profile():
    return render_template_string(PROFILE_TEMPLATE, current_user=current_user)

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    try:
        user = User.query.get(current_user.id)
        
        # Primero, revisamos si se subió un archivo nuevo
        file = request.files.get('avatar_file')
        if file and file.filename: # Un archivo fue subido
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            filename = secure_filename(file.filename)
            if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f"avatar_{user.id}_{int(datetime.now().timestamp())}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                file.save(filepath)
                user.profile_photo = url_for('static', filename=f'uploads/{new_filename}')
        else:
            # Si no se subió un archivo, usamos el valor del campo oculto (de la galería de avatares)
            user.profile_photo = request.form.get('profile_photo', user.profile_photo)
        
        # Actualizamos el resto de los campos
        user.name = request.form.get('name', user.name)
        user.email = request.form.get('email', user.email)
        
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        
        db.session.commit()
        return redirect(url_for('profile'))
    except Exception as e:
        db.session.rollback()
        return str(e), 500

@app.route('/progress')
@login_required
def progress():
    categories = {
        'emociones': {
            'name': 'Desarrollo Emocional',
            'icon': '😊',
            'color': '#FF9800'
        },
        'conceptos': {
            'name': 'Conceptos Básicos',
            'icon': '📚',
            'color': '#4CAF50'
        },
        'entorno': {
            'name': 'Conocimiento del Entorno',
            'icon': '🌍',
            'color': '#2196F3'
        },
        'vida_diaria': {
            'name': 'Vida Diaria',
            'icon': '🏠',
            'color': '#8BC34A'
        },
        'comunicacion': {
            'name': 'Comunicación',
            'icon': '🗣️',
            'color': '#FFB300'
        }
    }
    
    progress_data = []
    for category_key, category_info in categories.items():
        progress = UserProgress.query.filter_by(
                user_id=current_user.id,
                category=category_key
        ).first()

        if progress:
            progress_data.append({
                'name': category_info['name'],
                'icon': category_info['icon'],
                'color': category_info['color'],
                'completed_cards': progress.completed_cards,
                'total_cards': progress.total_cards,
                'best_score': progress.score,
                'last_activity': progress.updated_at.strftime('%d/%m/%Y'),
                'progress': progress.percentage
            })
        else:
            progress_data.append({
                'name': category_info['name'],
                'icon': category_info['icon'],
                'color': category_info['color'],
                'completed_cards': 0,
                'total_cards': 3,
                'best_score': 0,
                'last_activity': 'Sin actividad',
                'progress': 0
            })
    
    return render_template_string(PROGRESS_TEMPLATE, progress_data=progress_data, current_user=current_user)

@app.route('/get-all-progress')
@login_required
def get_all_progress():
    try:
        progress_data = {}
        categories = [c.category for c in db.session.query(Flashcard.category).distinct()]
        
        for category in categories:
            progress = UserProgress.query.filter_by(
                user_id=current_user.id,
                category=category
            ).first()
            
            if progress:
                progress_data[category] = {
                    'score': progress.score,
                    'percentage': progress.percentage,
                    'completed_cards': progress.completed_cards,
                    'completed': progress.completed,
                    'last_activity': progress.updated_at.strftime('%d/%m/%Y')
                }
            else:
                progress_data[category] = {
                    'score': 0,
                    'percentage': 0,
                    'completed_cards': 0,
                    'completed': False,
                    'last_activity': 'Sin actividad'
                }
        
        return jsonify(progress_data)
    except Exception as e:
        print(f"Error getting progress: {str(e)}")
        return jsonify({'error': str(e)}), 500

def init_flashcards():
    default_cards = {
        'emociones': [
            {
                'question': '¿Cómo te sientes cuando ves esta cara?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Grinning%20face/3D/grinning_face_3d.png',
                'options': ['Feliz', 'Triste', 'Enojado', 'Sorprendido'],
                'correct_option': 0,
                'feedback': '¡Muy bien! Cuando alguien sonríe así, está feliz y contento.'
            },
            {
                'question': '¿Qué emoción muestra esta cara?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Crying%20face/3D/crying_face_3d.png',
                'options': ['Feliz', 'Triste', 'Enojado', 'Sorprendido'],
                'correct_option': 1,
                'feedback': '¡Correcto! Es importante reconocer cuando alguien está triste para poder ayudar.'
            },
            {
                'question': '¿Qué emoción expresa esta cara?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Angry%20face/3D/angry_face_3d.png',
                'options': ['Feliz', 'Triste', 'Enojado', 'Sorprendido'],
                'correct_option': 2,
                'feedback': '¡Excelente! Reconocer cuando alguien está enojado nos ayuda a entender sus sentimientos.'
            }
        ],
        'conceptos': [
            {
                'question': '¿Qué número viene después del 2?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Keycap%203/3D/keycap_3_3d.png',
                'options': ['3', '4', '2', '1'],
                'correct_option': 0,
                'feedback': '¡Excelente! El número 3 viene después del 2. ¡Estás aprendiendo a contar muy bien!'
            },
            {
                'question': '¿Cuál es el primer número?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Keycap%201/3D/keycap_1_3d.png',
                'options': ['1', '2', '3', '4'],
                'correct_option': 0,
                'feedback': '¡Correcto! El número 1 es el primero que usamos para contar. ¡Muy bien hecho!'
            },
            {
                'question': '¿Qué número está entre el 1 y el 3?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Keycap%202/3D/keycap_2_3d.png',
                'options': ['2', '4', '1', '3'],
                'correct_option': 0,
                'feedback': '¡Perfecto! El número 2 está entre el 1 y el 3. ¡Eres muy inteligente!'
            }
        ],
        'entorno': [
            {
                'question': '¿Qué animal es este?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Dog%20face/3D/dog_face_3d.png',
                'options': ['Perro', 'Gato', 'Conejo', 'Pájaro'],
                'correct_option': 0,
                'feedback': '¡Correcto! Es un perro, un animal doméstico muy común.'
            },
            {
                'question': '¿Qué clima representa esta imagen?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Sun/3D/sun_3d.png',
                'options': ['Soleado', 'Lluvioso', 'Nublado', 'Nevado'],
                'correct_option': 0,
                'feedback': '¡Muy bien! Es un día soleado.'
            },
            {
                'question': '¿Qué fruta es esta?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Red%20apple/3D/red_apple_3d.png',
                'options': ['Manzana', 'Naranja', 'Plátano', 'Pera'],
                'correct_option': 0,
                'feedback': '¡Excelente! Es una manzana roja.'
            }
        ],
        'vida_diaria': [
            {
                'question': '¿Qué debes hacer antes de comer?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Soap/3D/soap_3d.png',
                'options': ['Lavar las manos', 'Dormir', 'Correr', 'Jugar'],
                'correct_option': 0,
                'feedback': '¡Correcto! Siempre debemos lavar las manos antes de comer.'
            },
            {
                'question': '¿Qué usas para cepillarte los dientes?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Toothbrush/3D/toothbrush_3d.png',
                'options': ['Cepillo de dientes', 'Cuchara', 'Lápiz', 'Jabón'],
                'correct_option': 0,
                'feedback': '¡Muy bien! El cepillo de dientes es para limpiar los dientes.'
            },
            {
                'question': '¿Qué haces después de despertarte?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Alarm%20clock/3D/alarm_clock_3d.png',
                'options': ['Levantarse', 'Dormir más', 'Ver TV', 'Comer dulces'],
                'correct_option': 0,
                'feedback': '¡Exacto! Después de despertarte, debes levantarte.'
            }
        ],
        'comunicacion': [
            {
                'question': '¿Qué puedes hacer cuando necesitas ayuda?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Raising%20hand/3D/raising_hand_3d.png',
                'options': ['¿Me ayudas, por favor?', 'Adiós', 'Gracias', 'Nada'],
                'correct_option': 0,
                'feedback': '¡Muy bien! Pedir ayuda es importante cuando la necesitas.'
            },
            {
                'question': '¿Qué debes hacer cuando alguien te habla?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Ear/3D/ear_3d.png',
                'options': ['Escuchar', 'Ignorar', 'Correr', 'Dormir'],
                'correct_option': 0,
                'feedback': '¡Correcto! Escuchar es importante para comunicarnos.'
            },
            {
                'question': '¿Qué puedes decir para saludar a alguien?',
                'image_url': 'https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Waving%20hand/3D/waving_hand_3d.png',
                'options': ['Hola', 'No', 'Silencio', 'Corre'],
                'correct_option': 0,
                'feedback': '¡Perfecto! Decir "Hola" es una forma amable de saludar.'
            }
        ]
    }

    for category, cards in default_cards.items():
        for card in cards:
            existing_card = Flashcard.query.filter_by(
                category=category,
                question=card['question']
            ).first()
            
            if not existing_card:
                new_card = Flashcard(
                    category=category,
                    question=card['question'],
                    image_url=card['image_url'],
                    options=json.dumps(card['options'], ensure_ascii=False),
                    correct_option=card['correct_option'],
                    feedback=card['feedback']
                )
                db.session.add(new_card)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing flashcards: {e}")

@app.route('/api/flashcards/<category>')
@login_required
def get_flashcards(category):
    cards = Flashcard.query.filter_by(category=category).all()
    cards_data = []
    for card in cards:
        try:
            # Forzamos la lectura de los datos como JSON.
            # Esto es más seguro porque init_flashcards ahora SIEMPRE guarda como JSON.
            options_list = json.loads(card.options)
        except (json.JSONDecodeError, TypeError):
            # Si algo sale mal, se omite la tarjeta para no bloquear la app.
            print(f"Error al decodificar las opciones para la tarjeta {card.id}: {card.options}")
            continue

        cards_data.append({
            'id': card.id,
            'question': card.question,
            'image_url': card.image_url,
            'options': options_list,
            'correct_option': card.correct_option,
            'feedback': card.feedback
        })
    return jsonify(cards_data)

def setup_database(app_instance):
    """Crea la base de datos y las tablas si no existen."""
    db_path = app_instance.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if not os.path.exists(db_path):
        with app_instance.app_context():
            print("Base de datos no encontrada. Creando y poblando...")
            db.create_all()
            init_flashcards()
            print("Base de datos creada exitosamente.")

if __name__ == '__main__':
    setup_database(app)
    app.run(debug=True) 