from flask import Flask, request
from flask_restful import Resource, Api, abort, fields, marshal
from functools import wraps
from iformat import iprint

from utils import default501, _always_in

app = Flask(__name__)
api = Api(app)

message_fields = {
    "message_id": fields.Integer,
    "convo_id": fields.Integer,
    "user_id": fields.Integer,
    "content": fields.String
}

class MessageList:
    def __init__(self):
        self.message_id = -1
        self.messages = []

    def _get_next_message_id(self):
        self.message_id += 1
        return self.message_id

    def query_filter(func):
        def wrapper(self, start=0, end=None, max_results=None, convo_ids=_always_in(), user_ids=_always_in(), message_ids=None):
            iprint(self.messages[start:end])
            iprint(f"start: {start}, end: {end}, max_results: {max_results}, convo_ids: {convo_ids}, user_ids: {user_ids}, message_ids: {message_ids}")
            if message_ids:
                res = list(filter(lambda m: m.message_id in message_ids, self.messages[start:end]))
                iprint("Using message_ids", res)
            else:
                res = list(filter(lambda m: m.convo_id in convo_ids and m.user_id in user_ids, self.messages[start:end]))
                iprint("Using convo_ids and user_ids", res)
            max_results = len(res) if max_results == None else max_results
            return func(self, res[:max_results])
        return wrapper

    @query_filter
    def query_get(self, messages):
        return messages

    def query_add(self, message):
        message.message_id = self._get_next_message_id()
        self.messages.append(message)
        return message

    def query_update(self, message_id, content):
        for message in self.messages:
            if message.message_id == message_id:
                message.content = content
                return message
        return None

    @query_filter
    def query_delete(self, messages):
        for message in messages:
            self.messages.remove(message)

msgs_list = MessageList()

class Message(default501):
    def get(self, message_id):
        self = msgs_list.query_get(message_ids=[message_id])
        if self is None:
            return {"error": f"Message {message_id} does not exist"}, 404
        return marshal(self, message_fields)

class Messages(default501):
    def get(self):
        try:
            message_ids = [int(id) for id in request.args.get("message_ids", "").split(",") if id]
        except Exception as e:
            print(e)
            iprint(e.with_traceback(None))
            return {"error": "Invalid value for message_ids"}, 400
        try:
            convo_ids = [int(id) for id in request.args.get("convo_ids", "").split(",") if id] or _always_in()
        except ValueError:
            return {"error": "Invalid value for convo_ids"}, 400
        try:
            user_ids = [int(id) for id in request.args.get("user_ids", "").split(",") if id] or _always_in()
        except ValueError:
            return {"error": "Invalid value for user_ids"}, 400
        try:
            start = int(request.args.get("start", 0))
        except ValueError:
            return {"error": "Invalid value for start"}, 400
        try:
            end = int(v) if (v:=request.args.get("end", None)) else None
        except ValueError:
            return {"error": "Invalid value for end"}, 400

        print(f"message_ids: {message_ids}, convo_ids: {convo_ids}, user_ids: {user_ids}, start: {start}, end: {end}")
        return [marshal(m, message_fields) for m in msgs_list.query_get(start=start, end=end, convo_ids=convo_ids, user_ids=user_ids, message_ids=message_ids)]

    def post(self):
        self.convo_id = int(request.json.get("convo_id"))
        self.user_id = int(request.json.get("user_id"))
        self.content = request.json.get("content")
        if self.convo_id is None or self.user_id is None or self.content is None:
            return {"error": "Missing required fields"}, 400
        return msgs_list.query_add(self).message_id, 201

class User(default501):
    pass

class Users(default501):
    pass

class Convo(default501):
    pass

class Convos(default501):
    pass

class ConvoUser(default501):
    pass

class ConvoUsers(default501):
    pass

api.add_resource(Message, "/messages/<int:message_id>", endpoint="message")
api.add_resource(Messages, "/messages", endpoint="messages")

api.add_resource(User, "/user/<int:user_id>", endpoint="user")
api.add_resource(Users, "/users", endpoint="users")

api.add_resource(Convo, "/convo/<int:convo_id>", endpoint="convo")
api.add_resource(Convos, "/convos", endpoint="convos")

api.add_resource(ConvoUser, "/convo/<int:convo_id>/user/<int:user_id>", endpoint="convo_user")
api.add_resource(ConvoUsers, "/convo/<int:convo_id>/users", endpoint="convo_users")

@app.errorhandler(404)
def page_not_found(e):
    return {"error": "The requested URL was not found."}, 404

if __name__ == "__main__":
    app.run()
