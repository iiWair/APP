# run.py
import sys
print(sys.path)

from app import create_app  # ← C'est ici que Python cherche dans app/__init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

