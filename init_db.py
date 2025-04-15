from app import app, db  # Import from your app.py

# This creates tables inside the application context
with app.app_context():
    db.create_all()
    print("✅ todo.db created successfully!")
