from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Convo(Resource):
    def get(self):
        return {
            "convo_id": 0,
            "name": "Conversation 0",
            "user_ids": [0, 1, 2],
            "message_ids": [0, 1, 2]
        }

    def post(self, convo_id, name, user_ids, message_ids):
        return {
            "convo_id": convo_id,
            "name": name,
            "user_ids": user_ids,
            "message_ids": message_ids
        }

    def put(self, convo_id, name, user_ids, message_ids):
        return {
            "convo_id": convo_id,
            "name": name,
            "user_ids": user_ids,
            "message_ids": message_ids
        }

    def delete(self, convo_id):
        return {
            "convo_id": convo_id
        }
    
class Message(Resource):
    def get(self):
        return {
            "message_id": 0,
            "text": "Hello, World!",
            "user_id": 0
        }

    def post(self, message_id, text, user_id):
        return {
            "message_id": message_id,
            "text": text,
            "user_id": user_id
        }

    def put(self, message_id, text, user_id):
        return {
            "message_id": message_id,
            "text": text,
            "user_id": user_id
        }

    def delete(self, message_id):
        return {
            "message_id": message_id
        }

class User(Resource):
    def get(self):
        return {
            "user_id": 0,
            "name": "User 0",
            "email": "test@example.com"
        }

    def post(self, user_id, name, email):
        return {
            "user_id": user_id,
            "name": name,
            "email": email
        }

    def put(self, user_id, name, email):
        return {
            "user_id": user_id,
            "name": name,
            "email": email
        }

    def delete(self, user_id):
        return {
            "user_id": user_id
        }


api.add_resource(Convo, '/convo/<int:convo_id>')
api.add_resource(Message, '/message/<int:message_id>')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)