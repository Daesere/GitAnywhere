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
    
class Coordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude_1 = db.Column(db.Float, nullable=False)
    longitude_1 = db.Column(db.Float, nullable=False)
    latitude_2 = db.Column(db.Float, nullable=False)
    longitude_2 = db.Column(db.Float, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'latitude_1': self.latitude_1,
            'longitude_1': self.longitude_1,
            'latitude_2': self.latitude_2,
            'longitude_2': self.longitude_2

        }
    
class Path(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html_path = db.Column(db.String(100), nullable=False)
    def to_json(self):
        return {
            'id': self.id,
            'htmlPath': self.html_path
        }