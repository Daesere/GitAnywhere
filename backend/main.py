 # CREATE READ UPDATE DELETE - CRUD
from flask import request, jsonify
from config import app, db
from models import User

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
 
    app.run(debug=True)