#!/usr/bin/env python3
"""
Script de configuración automática para el Sistema de Aprendizaje para Niños con Autismo
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def create_virtual_environment():
    """Crea el entorno virtual"""
    if os.path.exists("venv"):
        print("ℹ️ Entorno virtual ya existe")
        return True
    
    return run_command("python -m venv venv", "Creando entorno virtual")

def activate_virtual_environment():
    """Activa el entorno virtual"""
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\activate"
    else:
        activate_script = "source venv/bin/activate"
    
    print(f"🔧 Para activar el entorno virtual, ejecuta:")
    print(f"   {activate_script}")
    return True

def install_dependencies():
    """Instala las dependencias"""
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependencias")

def initialize_database():
    """Inicializa la base de datos"""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} init_database.py", "Inicializando base de datos")

def create_env_file():
    """Crea el archivo .env si no existe"""
    if os.path.exists(".env"):
        print("ℹ️ Archivo .env ya existe")
        return True
    
    env_content = """# Configuración del Sistema de Aprendizaje para Niños con Autismo
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-cambia-en-produccion
DATABASE_URL=sqlite:///autism_learning.db
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def main():
    """Función principal del setup"""
    print("🚀 Configurando Sistema de Aprendizaje para Niños con Autismo")
    print("=" * 60)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear entorno virtual
    if not create_virtual_environment():
        sys.exit(1)
    
    # Activar entorno virtual (instrucciones)
    activate_virtual_environment()
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n⚠️ Error instalando dependencias. Intenta activar el entorno virtual primero:")
        if platform.system() == "Windows":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Crear archivo .env
    create_env_file()
    
    # Inicializar base de datos
    if not initialize_database():
        print("\n⚠️ Error inicializando base de datos. Intenta ejecutar manualmente:")
        if platform.system() == "Windows":
            print("   venv\\Scripts\\python init_database.py")
        else:
            print("   venv/bin/python init_database.py")
        sys.exit(1)
    
    print("\n🎉 ¡Configuración completada exitosamente!")
    print("=" * 60)
    print("\n📋 Próximos pasos:")
    print("1. Activa el entorno virtual:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("2. Ejecuta la aplicación:")
    print("   python app.py")
    
    print("3. Abre tu navegador en:")
    print("   http://127.0.0.1:5000")
    
    print("\n👤 Usuario demo:")
    print("   Email: demo@example.com")
    print("   Contraseña: demo123")
    
    print("\n📚 Para más información, consulta el README.md")
    print("🔧 Para problemas, revisa los logs o crea un issue en GitHub")

if __name__ == "__main__":
    main() 