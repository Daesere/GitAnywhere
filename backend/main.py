 # CREATE READ UPDATE DELETE - CRUD
from flask import request, jsonify
from config import app, db
from models import User, Coordinates, Path
import gee_data
## USER LIST
# READ
@app.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({"users": [user.to_json() for user in users]})

# CREATE
@app.route("/create_user", methods=['POST'])
def create_user():
    first_name = request.json.get("firstName")
    weight = request.json.get("weight")
    height = request.json.get("height")

    if not first_name or not weight or not height:
        return (jsonify({"message": "Invalid data"}), 400,)
    
    new_user = User(first_name=first_name, weight=weight, height=height)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!"}), 201

# UPDATE
@app.route("/update_user/<int:user_id>", methods=['PATCH'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    user.first_name = data.get("firstName", user.first_name)
    user.weight = data.get("weight", user.weight)
    user.height = data.get("height", user.height)

    db.session.commit()

    return jsonify({"message": "User updated"}), 200

# DELETE
@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200

## COORDINATES
# READ Coordinates
@app.route("/coords", methods=['GET'])
def get_coords():
    coords = Coordinates.query.all()
    return jsonify({"coords": [coord.to_json() for coord in coords]})

#Create coord object
@app.route("/create_coord", methods=['POST'])
def create_coord():    
    longitude_1 = request.json.get("longitude_1")
    latitude_1 = request.json.get("latitude_1")
    longitude_2 = request.json.get("longitude_2")
    latitude_2 = request.json.get("latitude_2")

    if not longitude_1 or not latitude_1 or not longitude_2 or not latitude_2:
        return (jsonify({"message": "Missing coords"}), 400,)
    
    new_coord = Coordinates(longitude_1=longitude_1, latitude_1=latitude_1, longitude_2=longitude_2, latitude_2=latitude_2)

    try:
        db.session.add(new_coord)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Coord created!"}), 201

# DELETE
@app.route("/delete_coord", methods=["DELETE"])
def delete_coord():
    coord = Coordinates.query.first()

    if not coord:
        return jsonify({"message": "Already Clear"}), 404
    
    db.session.delete(coord)
    db.session.commit()

    return jsonify({"message": "Coord deleted"}), 200

### PATHS
#READ Recent Path
@app.route("/paths", methods=['GET'])
def get_paths():
    paths = Path.query.first()
    if not paths:
        return jsonify({"message": "No paths found"})
    return jsonify({"paths": [path.to_json() for path in paths]})

#Create path
@app.route("/create_path/<int:coord_id>", methods=['POST'])
def create_path(coord_id):
    coord = Coordinates.query.get(coord_id)
    if not coord:
        return jsonify({"message": "Coord not found"}), 404
    
    extra = request.args.get("extra")
    if extra:
        user = User.query.get(extra)
    if user:
        weight = user.weight
        height = user.height
    else:
        weight = 70
        height = 1.70

    coord_tuple = ((coord.longitude_1, coord.latitude_1), (coord.longitude_2, coord.latitude_2), weight, height)
    #GET PATH WITH COOL FUNCTION
    new_path = gee_data.create_map(coord_tuple)
    
    try:
        db.session.add(new_path)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Path created!!"}), 201
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
 
    app.run(debug=True)