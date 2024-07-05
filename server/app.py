from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order.
# POST /messages: creates a new message with a body and username from params, and returns the newly created post as JSON.
# PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
# DELETE /messages/<int:id>: deletes the message from the database.

@app.route('/messages', methods=['GET'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    if request.method == 'POST':
        data = request.get_json()
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()
    return jsonify(new_message.to_dict())

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_messages_by_id(id):
    if request.method == 'PATCH':
        message = db.session.get(Message, id)
        data = request.get_json()
        message.body = data.get('body', message.body)
        db.session.commit()
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_messages_by_id(id):
    if request.method == 'DELETE':
        message = db.session.get(Message, id)
        db.session.delete(message)
        db.session.commit()

if __name__ == '__main__':
    app.run(port=5555)
