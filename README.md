# 🧩 Sistema de Aprendizaje para Niños con Autismo

Una plataforma web interactiva diseñada específicamente para ayudar en el aprendizaje de niños con autismo, enfocándose en el desarrollo de habilidades emocionales, cognitivas y sociales.

## 🌟 Características Principales

### 🎯 Áreas de Aprendizaje
- **Desarrollo Emocional**: Reconocimiento de emociones y expresiones faciales
- **Conceptos Básicos**: Números, colores y formas
- **Conocimiento del Entorno**: Animales, clima y naturaleza
- **Vida Diaria**: Rutinas y actividades cotidianas
- **Comunicación**: Habilidades de comunicación básicas

### 🎮 Funcionalidades
- ✅ Sistema de autenticación seguro
- ✅ Dashboard interactivo y personalizado
- ✅ Tarjetas de aprendizaje (flashcards) con audio
- ✅ Seguimiento de progreso en tiempo real
- ✅ Interfaz adaptada para niños con autismo
- ✅ Diseño responsivo y accesible
- ✅ Pausas sensoriales y ayuda contextual
- ✅ Sistema de avatares personalizables

### ♿ Características de Accesibilidad
- Interfaz simplificada y clara
- Alto contraste para mejor visibilidad
- Animaciones reducidas para evitar distracciones
- Botones grandes y fáciles de usar
- Instrucciones claras y concisas
- Soporte para síntesis de voz

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Opción 1: Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/sistema-aprendizaje-autismo.git
cd sistema-aprendizaje-autismo
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar el entorno virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Inicializar la base de datos**
```bash
python init_database.py
```

6. **Ejecutar la aplicación**
```bash
python app.py
```

7. **Abrir en el navegador**
```
http://127.0.0.1:5000
```

### Opción 2: Usando Docker

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/sistema-aprendizaje-autismo.git
cd sistema-aprendizaje-autismo
```

2. **Construir y ejecutar con Docker Compose**
```bash
docker-compose up --build
```

3. **Abrir en el navegador**
```
http://localhost:5000
```

## 👤 Usuario Demo

Para probar la aplicación rápidamente:
- **Email**: `demo@example.com`
- **Contraseña**: `demo123`

## 🏗️ Estructura del Proyecto

```
sistema-aprendizaje-autismo/
├── app.py                 # Aplicación principal Flask
├── config.py             # Configuraciones de la aplicación
├── init_database.py      # Script de inicialización de BD
├── requirements.txt      # Dependencias de Python
├── Dockerfile           # Configuración de Docker
├── docker-compose.yml   # Orquestación de contenedores
├── .github/             # GitHub Actions (CI/CD)
├── static/              # Archivos estáticos
│   └── uploads/         # Archivos subidos por usuarios
├── templates/           # Plantillas HTML (integradas en app.py)
└── README.md           # Este archivo
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask**: Framework web ligero y flexible
- **SQLAlchemy**: ORM para manejo de base de datos
- **Flask-Login**: Manejo de autenticación de usuarios
- **Flask-CORS**: Soporte para CORS

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **JavaScript (ES6+)**: Interactividad del lado del cliente
- **Poppins Font**: Tipografía moderna y legible
- **Web Speech API**: Síntesis de voz

### Base de Datos
- **SQLite**: Base de datos ligera (desarrollo)
- **PostgreSQL**: Base de datos robusta (producción)

### DevOps
- **Docker**: Containerización
- **GitHub Actions**: CI/CD pipeline
- **Flake8**: Linting de código
- **Pytest**: Testing automatizado

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-super-segura
DATABASE_URL=sqlite:///autism_learning.db
```

### Configuración de Producción

Para despliegue en producción:

1. Cambiar `FLASK_ENV=production`
2. Usar una clave secreta fuerte
3. Configurar una base de datos PostgreSQL
4. Habilitar HTTPS
5. Configurar logging

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest flake8

# Ejecutar tests
pytest

# Ejecutar linting
flake8 .
```

## 📊 Monitoreo y Logs

La aplicación incluye:
- Logging estructurado
- Métricas de rendimiento
- Monitoreo de errores
- Health checks

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Sesiones seguras con Flask-Login
- ✅ Protección CSRF
- ✅ Validación de entrada
- ✅ Sanitización de datos
- ✅ Headers de seguridad

## 🤝 Contribuir

¡Tus contribuciones son bienvenidas! Por favor:

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Guías de Contribución

- Sigue las convenciones de código existentes
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Mantén la accesibilidad en mente

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **Microsoft Fluent UI Emoji**: Emojis utilizados en las tarjetas
- **DiceBear**: Avatares generados automáticamente
- **ARASAAC**: Pictogramas de comunicación
- **Comunidad de desarrolladores**: Por el feedback y contribuciones

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:

- 📧 **Email**: soporte@sistema-autismo.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/tu-usuario/sistema-aprendizaje-autismo/issues)
- 📖 **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/sistema-aprendizaje-autismo/wiki)

## 🗺️ Roadmap

### Próximas Funcionalidades
- [ ] Sistema de logros y recompensas
- [ ] Modo multijugador para terapia grupal
- [ ] Integración con dispositivos móviles
- [ ] Análisis avanzado de progreso
- [ ] Personalización de contenido por terapeuta
- [ ] Exportación de reportes de progreso

### Mejoras Técnicas
- [ ] API REST completa
- [ ] Cache distribuido con Redis
- [ ] Microservicios
- [ ] Machine Learning para personalización
- [ ] PWA (Progressive Web App)

---

**¡Gracias por usar nuestro Sistema de Aprendizaje para Niños con Autismo!** 🌟

*Desarrollado con ❤️ para hacer el aprendizaje más accesible y efectivo.* 