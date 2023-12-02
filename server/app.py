from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        
        response = make_response(
            jsonify([message.to_dict() for message in messages]), 200
        )

        return response
    
    elif request.method == 'POST':
        body = request.json['body']
        username = request.json['username']
        message = Message(body=body, username=username)
        
        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()), 201
        )

        return response
        

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def update_message(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        body = request.get_json()
        for key in body:
            setattr(message, key, body[key])
          
        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()), 200
        )

        return response

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response = make_response(
            jsonify({'message': 'deleted'}), 200
        )

        return response


if __name__ == '__main__':
    app.run(port=5555)