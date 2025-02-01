from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    weight = db.Column(db.INT(), unique=False, nullable=False)
    height = db.Column(db.INT(), unique=False, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'weight': self.weight,
            'height': self.height
        }