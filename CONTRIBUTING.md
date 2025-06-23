# 🤝 Guías de Contribución

¡Gracias por tu interés en contribuir al Sistema de Aprendizaje para Niños con Autismo! Tu ayuda es invaluable para hacer esta plataforma más accesible y efectiva.

## 📋 Tabla de Contenidos

- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reporte de Bugs](#reporte-de-bugs)
- [Solicitud de Funcionalidades](#solicitud-de-funcionalidades)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## 🚀 Cómo Contribuir

### Tipos de Contribuciones

Aceptamos varios tipos de contribuciones:

- 🐛 **Reporte de bugs**
- 💡 **Solicitud de nuevas funcionalidades**
- 📝 **Mejoras en la documentación**
- 🎨 **Mejoras en la interfaz de usuario**
- ⚡ **Optimizaciones de rendimiento**
- 🔒 **Mejoras de seguridad**
- ♿ **Mejoras de accesibilidad**

### Antes de Contribuir

1. **Revisa los issues existentes** para evitar duplicados
2. **Lee la documentación** del proyecto
3. **Prueba la aplicación** para entender su funcionamiento
4. **Asegúrate de que tu contribución** sea relevante para el proyecto

## 🛠️ Configuración del Entorno de Desarrollo

### Prerrequisitos

- Python 3.8 o superior
- Git
- Un editor de código (VS Code, PyCharm, etc.)

### Pasos de Configuración

1. **Fork el repositorio**
```bash
# Ve a GitHub y haz fork del repositorio
# Luego clona tu fork
git clone https://github.com/tu-usuario/sistema-aprendizaje-autismo.git
cd sistema-aprendizaje-autismo
```

2. **Configura el entorno de desarrollo**
```bash
# Ejecuta el script de configuración automática
python setup.py

# O configura manualmente
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_database.py
```

3. **Configura el upstream**
```bash
git remote add upstream https://github.com/original-usuario/sistema-aprendizaje-autismo.git
```

4. **Crea una rama para tu feature**
```bash
git checkout -b feature/tu-nueva-funcionalidad
```

## 📏 Estándares de Código

### Python

- **PEP 8**: Sigue las convenciones de estilo de Python
- **Docstrings**: Documenta todas las funciones y clases
- **Type hints**: Usa type hints cuando sea posible
- **Manejo de errores**: Implementa manejo de errores apropiado

### JavaScript

- **ES6+**: Usa características modernas de JavaScript
- **Comentarios**: Documenta funciones complejas
- **Nombres descriptivos**: Usa nombres de variables y funciones claros
- **Consistencia**: Mantén el estilo consistente con el código existente

### HTML/CSS

- **Semántica**: Usa elementos HTML semánticos
- **Accesibilidad**: Sigue las pautas WCAG 2.1
- **Responsive**: Asegúrate de que funcione en móviles
- **Organización**: Mantén el CSS organizado y comentado

### Ejemplo de Código Python

```python
def calculate_progress(user_id: int, category: str) -> dict:
    """
    Calcula el progreso del usuario en una categoría específica.
    
    Args:
        user_id (int): ID del usuario
        category (str): Categoría de aprendizaje
        
    Returns:
        dict: Diccionario con el progreso calculado
        
    Raises:
        ValueError: Si el user_id es inválido
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id debe ser un entero positivo")
    
    # Tu lógica aquí
    return {"progress": 75, "completed": True}
```

## 🔄 Proceso de Pull Request

### 1. Preparación

- Asegúrate de que tu código funcione correctamente
- Ejecuta los tests: `pytest`
- Ejecuta el linter: `flake8 .`
- Actualiza la documentación si es necesario

### 2. Commit

```bash
# Agrega tus cambios
git add .

# Haz commit con un mensaje descriptivo
git commit -m "feat: agregar nueva funcionalidad de progreso visual

- Implementa barra de progreso animada
- Agrega indicadores de completado
- Mejora la experiencia de usuario
- Cierra #123"
```

### 3. Push y Pull Request

```bash
# Push a tu fork
git push origin feature/tu-nueva-funcionalidad

# Ve a GitHub y crea un Pull Request
```

### 4. Descripción del Pull Request

Usa esta plantilla:

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Mejora de documentación
- [ ] Refactorización
- [ ] Test

## Cambios realizados
- Lista de cambios específicos
- Incluye capturas de pantalla si es relevante

## Testing
- [ ] Tests unitarios pasan
- [ ] Tests de integración pasan
- [ ] Pruebas manuales realizadas

## Checklist
- [ ] Mi código sigue los estándares del proyecto
- [ ] He actualizado la documentación
- [ ] He agregado tests para nuevas funcionalidades
- [ ] Todos los tests pasan
- [ ] He verificado la accesibilidad

## Screenshots (si aplica)
[Agrega capturas de pantalla aquí]

## Issue relacionado
Closes #123
```

## 🐛 Reporte de Bugs

### Antes de Reportar

1. **Busca en los issues existentes** para ver si ya fue reportado
2. **Prueba en la versión más reciente** del código
3. **Verifica que no sea un problema de configuración**

### Plantilla de Bug Report

```markdown
## Descripción del Bug
Descripción clara y concisa del bug.

## Pasos para Reproducir
1. Ve a '...'
2. Haz clic en '...'
3. Desplázate hacia abajo hasta '...'
4. Ve el error

## Comportamiento Esperado
Descripción de lo que debería suceder.

## Comportamiento Actual
Descripción de lo que realmente sucede.

## Screenshots
Si aplica, agrega capturas de pantalla.

## Información del Sistema
- OS: [ej. Windows 10, macOS, Ubuntu]
- Navegador: [ej. Chrome, Firefox, Safari]
- Versión: [ej. 22]
- Python: [ej. 3.11.0]

## Información Adicional
Cualquier contexto adicional sobre el problema.
```

## 💡 Solicitud de Funcionalidades

### Antes de Solicitar

1. **Verifica que no exista** una funcionalidad similar
2. **Considera el impacto** en la accesibilidad
3. **Piensa en la implementación** y complejidad

### Plantilla de Feature Request

```markdown
## Descripción de la Funcionalidad
Descripción clara de la funcionalidad deseada.

## Problema que Resuelve
Explicación de por qué esta funcionalidad es necesaria.

## Solución Propuesta
Descripción de cómo debería funcionar.

## Alternativas Consideradas
Otras soluciones que consideraste.

## Información Adicional
Capturas de pantalla, mockups, etc.
```

## ❓ Preguntas Frecuentes

### ¿Cómo puedo empezar si soy nuevo?

1. **Revisa los issues con la etiqueta "good first issue"**
2. **Lee la documentación** del proyecto
3. **Únete a las discusiones** en los issues
4. **Haz preguntas** en los issues o discussions

### ¿Qué hago si mi PR no es revisado?

- **Sé paciente**: Los maintainers revisan PRs regularmente
- **Verifica que tu PR** siga las guías
- **Agrega más contexto** si es necesario
- **Ping amigablemente** después de una semana

### ¿Cómo puedo mejorar mis chances de que mi PR sea aceptado?

- **Sigue las guías** de contribución
- **Escribe tests** para nuevas funcionalidades
- **Documenta** tus cambios
- **Mantén el enfoque** en una funcionalidad por PR
- **Sé respetuoso** en las discusiones

### ¿Puedo contribuir si no sé programar?

¡Absolutamente! Necesitamos ayuda con:

- **Documentación**: Mejorar el README, guías de usuario
- **Testing**: Probar la aplicación y reportar bugs
- **Diseño**: Sugerencias de UI/UX
- **Traducciones**: Ayudar con múltiples idiomas
- **Feedback**: Compartir experiencias de uso

## 📞 Contacto

Si tienes preguntas sobre cómo contribuir:

- 📧 **Email**: contribuciones@sistema-autismo.com
- 💬 **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/sistema-aprendizaje-autismo/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/tu-usuario/sistema-aprendizaje-autismo/issues)

## 🙏 Agradecimientos

Gracias a todos los contribuidores que hacen este proyecto posible. Tu trabajo ayuda a hacer el aprendizaje más accesible para niños con autismo.

---

**¡Gracias por contribuir!** 🌟 