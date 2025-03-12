from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class IndexedCollection:
    """
    A collection of items of a given instance type that can be accessed by ID.
    """
    def __init__(self, instance_type):
        """
        Initializes the collection and saves given instance type to be used for new items.
        """
        self._instance_type = instance_type
        self._collection = {}
        self._next_id = 0

    def _get_next_id(self):
        """
        Returns the next available ID for the collection, and increments the internal counter.
        """
        self._next_id += 1
        return self._next_id - 1

    def __getitem__(self, id):
        return self._collection.get(id)

    def __setitem__(self, id, value):
        self._collection[id] = value

    def __delitem__(self, id):
        del self._collection[id]

    def all(self):
        """
        Returns all items in the collection.
        """
        return self._collection

    def new(self, *args):
        """
        Creates a new instance of the collection's instance type and adds it to the collection.
        """
        id = self._get_next_id()
        self._collection[id] = self._instance_type(id, *args)

class Convo(Resource):
    """
    A conversation between multiple users with a given name.
    """
    def __init__(self, id, name, user_ids):
        """
        Initializes the conversation with the given ID, name, and user IDs.
        """
        self.id = id
        self.name = name
        self.user_ids = user_ids
    
    def get(self, convo_id = None):
        """
        Returns the conversation with the given ID, or all conversations if no ID is given.
        """
        print(f"Received GET request for convo id {convo_id}")
        return convos[convo_id] or convos.all()

    def post(self, convo_id = None):
        """
        Creates a new conversation with the given name and user IDs. If a conversation ID is given (endpoint='convo_user'), adds the user with the given ID to the conversation.
        """
        if request.endpoint == "convo_user":
            user_id = request.view_args["user_id"]
            print(f"Received POST request for convo id {convo_id} with args {user_id} (endpoint='convo_user')")
            convos[convo_id].user_ids.append(user_id)
        else:
            name = request.form.get("name")
            user_ids = request.form.get("user_ids", [])
            print(f"Received POST request for convo with args {name}, {user_ids}")
            convos.new(name, user_ids)

    def put(self, convo_id):
        """
        Updates the conversation with the given ID with the given name and user IDs.
        """
        name = request.form.get("name", convos[convo_id].name)
        user_ids = request.form.get("user_ids", convos[convo_id].user_ids)
        print(f"Received PUT request for convo id {convo_id} with args {name}, {user_ids}")
        convos[convo_id].name = name
        convos[convo_id].user_ids = user_ids

    def patch(self, convo_id):
        """
        Adds/removes the users with the given IDs to/from the conversation with the given ID.
        """
        add_user_ids = request.form.get("add_user_ids")
        remove_user_ids = request.form.get("remove_user_ids")
        print(f"Received PATCH request for convo id {convo_id} with args {add_user_ids}, {remove_user_ids}")
        convos[convo_id].user_ids.extend(add_user_ids)
        for user_id in remove_user_ids:
            convos[convo_id].user_ids.remove(user_id)


    def delete(self, convo_id):
        """
        Deletes the conversation with the given ID. If a user ID is given (endpoint='convo_user'), removes the user with the given ID from the conversation.
        """
        if request.endpoint == "convo_user":
            user_id = request.view_args["user_id"]
            print(f"Received DELETE request for convo id {convo_id} with args {user_id} (endpoint='convo_user')")
            convos[convo_id].user_ids.remove(user_id)
        else:
            print(f"Received DELETE request for convo id {convo_id}")
            del convos[convo_id]

class Convos(IndexedCollection):
    """
    A collection of conversations.
    """
    def __init__(self):
        super().__init__(Convo)

convos = Convos()

class Message(Resource):
    """
    A message sent by a user in a conversation.
    """
    def __init__(self, id, content, user_id, convo_id):
        """
        Initializes the message with the given ID, content, user ID, and conversation ID.
        """
        self.id = id
        self.content = content
        self.user_id = user_id
        self.convo_id = convo_id

    def get(self, message_id = None):
        """
        Returns the message with the given ID, or all messages if no ID is given.
        """
        print(f"Received GET request for message id {message_id}")
        return msgs[message_id] or msgs.all()

    def post(self, convo_id):
        """
        Creates a new message in the conversation with the given ID.
        """
        content = request.form.get("content")
        user_id = request.form.get("user_id")
        print(f"Received POST request for message in convo id {convo_id} with args {content}, {user_id}")
        msgs.append_new(convo_id, content, user_id)

    def put(self, message_id, convo_id = None):
        """
        Updates the content of the message with the given ID, or the message with the given ID in the conversation with the given ID. This method is faster when the conversation ID is known.
        """
        content = request.form.get("content", msgs.get_by_message_id(message_id).content)
        print(f"Received PUT request for message id {message_id}{f' in convo id {convo_id}' if convo_id else ''} with args {content}")
        if convo_id:
            msgs.get_by_convo_id(convo_id, message_id).content = content
        else:
            msgs.get_by_message_id(message_id).content = content

    def delete(self, message_id, convo_id = None):
        """
        Deletes the message with the given ID, or the message with the given ID in the conversation with the given ID. This method is faster when the conversation ID is known.
        """
        print(f"Received DELETE request for message id {message_id}")
        if convo_id:
            msgs.remove_by_convo_id(convo_id, message_id)
        else:
            msgs.remove_by_message_id(message_id)

class Messages(IndexedCollection):
    """
    A collection of messages.
    """
    def __init__(self):
        super().__init__(list)

    def append_to(self, id, value):
        """
        Appends a value to the list stored under the given conversation ID.
        """
        self._collection[id].append(value)
    
    def append_new(self, id, *args):
        """
        Creates a new message and appends it to the list stored under the given conversation ID.
        """
        self._collection[id].append(self._instance_type(self._get_next_id(), *args))

    def get_by_convo_id(self, convo_id, message_id = None):
        """
        Returns the message with the given ID in the conversation with the given ID, or all messages in the conversation if no message ID is given.
        """
        return self._collection[convo_id][message_id] or self._collection[convo_id].all()

    def get_by_message_id(self, message_id):
        """
        Returns the message with the given ID from any conversation. This method is slower than get_by_convo_id, and should only be used when the conversation ID is not known.
        """
        for convo in self._collection.values():
            for message in convo:
                if message.id == message_id:
                    return message
    
    def remove_by_convo_id(self, convo_id, message_id = None):
        """"
        Deletes the message with the given ID from the conversation with the given ID, or clears all messages from the conversation if no message ID is given.
        """
        if message_id:
            del self._collection[convo_id][message_id]
        else:
            del self._collection[convo_id]
    
    def remove_by_message_id(self, message_id):
        """
        Deletes the message with the given ID from any conversation. This method is slower than remove_by_convo_id, and should only be used when the conversation ID is not known.
        """
        for convo in self._collection.values():
            for message in convo:
                if message.id == message_id:
                    del convo[message_id]

msgs = Messages()

class User(Resource):
    """
    A user with a given name and email address.
    """
    def __init__(self, id, name, email):
        """
        Initializes the user with the given ID, name, and email address.
        """
        self.id = id
        self.name = name
        self.email = email
        self.active = True

    def get(self, user_id = None):
        """
        Returns the user with the given ID, or all users if no ID is given.
        """
        print(f"Received GET request for user id {user_id}")
        return users[user_id] or users.all()

    def post(self):
        """
        Creates a new user with the given name, email address, and active status (default True).
        """
        name = request.form.get("name")
        email = request.form.get("email")
        active = request.form.get("active", True)
        print(f"Received POST request for user with args {name}, {email}, {active}")
        users.new(name, email, active)

    def put(self, user_id):
        """
        Updates the user with the given ID with the given name and email address.
        """
        name = request.form.get("name", users[user_id].name)
        email = request.form.get("email", users[user_id].email)
        active = request.form.get("active", users[user_id].active)
        print(f"Received PUT request for user id {user_id} with args {name}, {email}, {active}")
        users[user_id].name = name
        users[user_id].email = email
        users[user_id].active = active

    def delete(self, user_id):
        """
        Deletes the user with the given ID.
        """
        print(f"Received DELETE request for user id {user_id}")
        del users[user_id]

class Users(IndexedCollection):
    """
    A collection of users.
    """
    def __init__(self):
        super().__init__(User)

users = Users()

api.add_resource(Convo, "/convos", "/convo/<int:convo_id>", endpoint="convo")
api.add_resource(Convo, "/convo/<int:convo_id>/users", "/convo/<int:convo_id>/user/<int:user_id>", endpoint="convo_user")
api.add_resource(Message, "/convo/<int:convo_id>/messages", "/convo/<int:convo_id>/message/<int:message_id>", "/message/<int:message_id>", endpoint="message")
api.add_resource(User, "/user/<int:user_id>", "/users", endpoint="user")

if __name__ == "__main__":
    app.run()