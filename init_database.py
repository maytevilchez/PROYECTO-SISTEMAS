#!/usr/bin/env python3
"""
Script para inicializar la base de datos del Sistema de Aprendizaje para Niños con Autismo
"""

import os
import json
from datetime import datetime
from app import app, db, User, UserProgress, Flashcard

def init_flashcards():
    """Inicializa las tarjetas de aprendizaje por defecto"""
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
                print(f"Agregada tarjeta: {card['question']} en categoría {category}")
    
    try:
        db.session.commit()
        print("✅ Tarjetas de aprendizaje inicializadas correctamente")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al inicializar tarjetas: {e}")

def create_sample_user():
    """Crea un usuario de ejemplo para testing"""
    from werkzeug.security import generate_password_hash
    
    existing_user = User.query.filter_by(email='demo@example.com').first()
    if not existing_user:
        sample_user = User(
            name='Usuario Demo',
            email='demo@example.com',
            password_hash=generate_password_hash('demo123'),
            profile_photo='https://api.dicebear.com/8.x/adventurer/svg?seed=Felix'
        )
        db.session.add(sample_user)
        db.session.commit()
        print("✅ Usuario demo creado: demo@example.com / demo123")
    else:
        print("ℹ️ Usuario demo ya existe")

def setup_database():
    """Configura la base de datos completa"""
    print("🚀 Iniciando configuración de la base de datos...")
    
    # Crear todas las tablas
    db.create_all()
    print("✅ Tablas creadas correctamente")
    
    # Crear carpeta de uploads si no existe
    upload_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print("✅ Carpeta de uploads creada")
    
    # Inicializar tarjetas
    init_flashcards()
    
    # Crear usuario demo
    create_sample_user()
    
    print("🎉 Base de datos configurada completamente!")

if __name__ == '__main__':
    with app.app_context():
        setup_database() 