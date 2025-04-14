from app import create_app, db
from app.models import Log

app = create_app()

with app.app_context():
    db.create_all()  # Creates the database and tables
    print("Database initialized!")