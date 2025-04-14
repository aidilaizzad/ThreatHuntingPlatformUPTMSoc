from . import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(50), nullable=False, default="Low")

    def _repr_(self):
        return f"<Log {self.id} - {self.message}>"