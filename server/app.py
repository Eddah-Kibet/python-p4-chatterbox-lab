# server/your_app.py
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

# Message routes
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = db.session.query(Message).all()
    return jsonify([message.to_dict() for message in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    if request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get('body'),
            username=data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def messages_by_id(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({"error": "Message not found"}), 404
    elif request.method == 'PATCH':
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
        if 'username' in data:
            message.username = data['username']
        db.session.commit()
        return jsonify(message.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return make_response('message not found', 404)
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response('message deleted', 200)

# Earthquake routes
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)
    if not earthquake:
        return jsonify({"error": "Earthquake not found"}), 404
    return jsonify(earthquake.to_dict()), 200

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = db.session.query(Earthquake).filter_by(magnitude=magnitude).all()
    return jsonify({
        "count": len(earthquakes),
        "quakes": [eq.to_dict() for eq in earthquakes]
    }), 200

if __name__ == '__main__':
    app.run(port=5555)