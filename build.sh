#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# El contexto de la aplicación es necesario para db.create_all()
echo "Running database setup..."
python -c "from app import app, db, init_flashcards; app.app_context().push(); db.create_all(); init_flashcards()"
echo "Database setup complete." 