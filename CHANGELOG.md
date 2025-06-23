# 📝 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sistema de badges para el README
- Script de configuración automática (`setup.py`)
- Configuración para despliegue en Render
- Guías de contribución completas
- Archivo de changelog
- Configuración de Docker y Docker Compose
- GitHub Actions para CI/CD
- Archivo de configuración separado (`config.py`)

### Changed
- README actualizado con información más completa
- Mejorada la documentación del proyecto
- Reorganizada la estructura de archivos

### Fixed
- Mejorado el manejo de errores en la inicialización de la base de datos

## [1.0.0] - 2024-01-15

### Added
- 🎉 **Lanzamiento inicial del Sistema de Aprendizaje para Niños con Autismo**
- Sistema de autenticación completo con registro e inicio de sesión
- Dashboard interactivo con 5 áreas de aprendizaje:
  - Desarrollo Emocional
  - Conceptos Básicos
  - Conocimiento del Entorno
  - Vida Diaria
  - Comunicación
- Sistema de flashcards interactivas con:
  - Imágenes de alta calidad (Microsoft Fluent UI Emoji)
  - Audio de síntesis de voz
  - Feedback inmediato y motivacional
  - Progreso visual en tiempo real
- Sistema de progreso y seguimiento:
  - Barras de progreso animadas
  - Estadísticas detalladas
  - Historial de actividad
- Perfil de usuario personalizable:
  - Avatares generados automáticamente (DiceBear)
  - Subida de fotos personalizadas
  - Edición de información personal
- Características de accesibilidad:
  - Interfaz simplificada y clara
  - Alto contraste para mejor visibilidad
  - Animaciones reducidas
  - Botones grandes y fáciles de usar
  - Pausas sensoriales
  - Botón de ayuda contextual
- Diseño responsivo para móviles y tablets
- Base de datos SQLite con 15 tarjetas de aprendizaje predefinidas
- Sistema de seguridad:
  - Contraseñas hasheadas con bcrypt
  - Sesiones seguras
  - Protección CSRF
  - Validación de entrada

### Technical Features
- Backend con Flask y SQLAlchemy
- Frontend con HTML5, CSS3 y JavaScript moderno
- Base de datos SQLite para desarrollo
- Sistema de templates integrado
- Manejo de archivos estáticos
- Configuración flexible para diferentes entornos

### User Experience
- Interfaz intuitiva y amigable para niños
- Mensajes motivacionales personalizados
- Sistema de recompensas visuales
- Navegación clara y consistente
- Carga rápida y rendimiento optimizado

## [0.9.0] - 2024-01-10

### Added
- Versión beta del sistema de flashcards
- Sistema básico de autenticación
- Interfaz de usuario inicial

### Changed
- Mejoras en el diseño responsivo
- Optimización del rendimiento

## [0.8.0] - 2024-01-05

### Added
- Primera versión del dashboard
- Sistema de base de datos básico
- Estructura del proyecto

### Fixed
- Correcciones menores en la interfaz

---

## Notas de Versión

### Convenciones de Versionado

Este proyecto usa [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH**
- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Nuevas funcionalidades compatibles hacia atrás
- **PATCH**: Correcciones de bugs compatibles hacia atrás

### Tipos de Cambios

- **Added**: Nuevas funcionalidades
- **Changed**: Cambios en funcionalidades existentes
- **Deprecated**: Funcionalidades que serán removidas
- **Removed**: Funcionalidades removidas
- **Fixed**: Correcciones de bugs
- **Security**: Mejoras de seguridad

### Contribuir al Changelog

Al hacer contribuciones, por favor:

1. Agrega tus cambios en la sección `[Unreleased]`
2. Usa los tipos de cambios apropiados
3. Sé específico sobre qué cambió
4. Incluye referencias a issues si aplica

### Ejemplo de Entrada

```markdown
### Added
- Nueva funcionalidad de exportación de progreso (#123)
- Soporte para múltiples idiomas

### Fixed
- Error en el cálculo de progreso (#124)
- Problema de rendimiento en móviles
```

---

**Para más información sobre los cambios, consulta los [commits de Git](https://github.com/tu-usuario/sistema-aprendizaje-autismo/commits).** 