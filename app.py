from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Convos():
    convos = []
    _next_id = 0

    def __getitem__(self, convo_id):
        for convo in self.convos:
            if convo.id == convo_id:
                return convo
        return None
            
    def _get_next_id(self):
        self._next_id += 1
        return self._next_id
    
    def all(self):
        return self.convos

    def get(self):
        return self.convos

    def post(self):
        name = request.form.get("name")
        user_ids = request.form.get("user_ids")
        print(f"Received POST request for convo with args {name}, {user_ids}")
        self.convos.append(Convo(self._get_next_id(), name, user_ids))

class Convo(Resource):
    def __init__(self, id, name, user_ids):
        self.id = id
        self.name = name
        self.user_ids = user_ids
        self.message_ids = []
    
    def get(self, convo_id):
        print(f"Received GET request for convo id {convo_id}")
        return Convos[convo_id] or Convos.all()

    def post(self):
        name = request.form.get("name")
        user_ids = request.form.get("user_ids")
        print(f"Received POST request for convo with args {name}, {user_ids}")
        convos.append(Convo(name, user_ids))

    def put(self, convo_id):
        name = request.form.get("name")
        user_ids = request.form.get("user_ids")
        message_ids = request.form.get("message_ids")
        print(f"Received PUT request for convo id {convo_id} with args {name}, {user_ids}, {message_ids}")
        return {
            "convo_id": convo_id,
            "name": name,
            "user_ids": user_ids,
            "message_ids": message_ids
        }

    def delete(self, convo_id):
        print(f"Received DELETE request for convo id {convo_id}")
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


api.add_resource(Convo, "/convo", "/convo/<int:convo_id>")
api.add_resource(Message, "/convo/<int:convo_id>/message/<int:message_id>", "/message/<int:message_id>")
api.add_resource(User, "/user/<int:user_id>")

if __name__ == "__main__":
    app.run()