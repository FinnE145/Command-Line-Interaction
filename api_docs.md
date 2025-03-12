# Command-Line Interaction API Documentation

## Overview:
#### Messages
- `/message` (`POST`) - Create a new message
- `/message/<message_id>` (`GET`, `PUT`, `DELETE`) - Retrieve, edit, and delete a specific message
- `/messages` (`GET`, `POST`, `DELETE`) - Bulk retrieve, create, and delete messages, with filters.

#### Users
- `/user` (`POST`) - Create a new user
- `/user/<user_id>` (`GET`, `PUT`, `DELETE`) - Retrieve, edit, and delete a specific user
- `/users` (`GET`, `POST`, `DELETE`) - Bulk retrieve, create, and delete users

#### Conversations
- `/convo` (`POST`) - Create a new conversation
- `/convo/<convo_id>` (`GET`, `PUT`, `DELETE`) - Retrieve, edit, and delete a specific conversation
- `/convos` (`GET`, `POST`, `DELETE`) - Bulk retrieve, create, and delete conversations

#### Conversation Messages
- `/convo/<convo_id>/message` (`POST`) - Create a new message in a conversation
- `/convo/<convo_id>/messages` (`GET`, `POST`, `PUT`, `DELETE`) - Bulk retrieve, create, update, and delete messages in a conversation

#### Conversation Users
- `/convo/<convo_id>/user/<user_id>` (`POST`, `DELETE`) - Add and remove a user from a conversation
- `/convo/<convo_id>/users` (`GET`, `POST`, `DELETE`) - Bulk retrieve, create, update, and delete users in a conversation

## Messages

#### `message` data type:
- `message_id` *`int`*: The ID of the message
- `convo_id` *`int`*: The ID of the conversation the message belongs to
- `user_id` *`int`*: The ID of the user who sent the message
- `content` *`string`*: The content of the message

#### `new_message` data type:
- `convo_id` *`int`*: The ID of the conversation the message belongs to
- `user_id` *`int`*: The ID of the user who sent the message
- `content` *`string`*: The content of the message

#### `message_filter` data type:
- [`start_index` *`int`*]: The index of the first message to retrieve. Can be negative to start from the most recent message. If not provided, retrieval starts from the beginning.
- [`end_index` *`int`*]: The index of the last message to retrieve. If not provided, retrieval continues to the end.
- [`convo_ids` *`list<int>`*]: A list of conversation IDs to retrieve messages from. Results are joined with OR. If not provided, messages from all conversations are retrieved.
- [`user_ids` *`list<int>`*]: A list of user IDs to retrieve messages from. Results are joined with OR. If not provided, messages from all users are retrieved.
- [`filter_mode` *`string`*]: The join mode between the above filters. Can be `'AND'` or `'OR'`. If not provided, AND is used.

### `/message`
- **POST**: Create a new message\
    <u>Data:</u>
    - `convo_id` *`int`*: The ID of the conversation the message belongs to
    - `user_id` *`int`*: The ID of the user sending the message
    - `content` *`string`*: The content of the message

    <u>Returns:</u>
    - `message_id` *`int`*: The ID of the newly created message

### `/message/<message_id:int>`
- **GET**: Retrieve info about the given message\
    <u>Returns:</u>
    - `message_id` *`int`*: The ID of the message
    - `convo_id` *`int`*: The ID of the conversation the message belongs to
    - `user_id` *`int`*: The ID of the user who sent the message
    - `content` *`string`*: The content of the message

- **PUT**: Update the message with the given ID\
    <u>Data:</u>
    - [`content` *`string`*]: The new content of the message. If not provided, the message will not be updated.

- **DELETE**: Delete the message with the given ID. This will remove it from its conversation.

### `/messages`
> Messages are sorted by their IDs, with the most recent messages having the highest IDs.
- **GET**: Bulk retrieve messages\
    <u>Data:</u>
    - [`message_ids` *`list<int>`*]: The IDs of the messages to retrieve. If not provided, all messages will be retrieved.\
    **OR**
    - [`filters` *`list<message_filter>`*]: A list of filters to apply to the messages. The results returned by each filter are joined with `OR`. If not provided, all messages will be retrieved.

    <u>Returns:</u>
    - `messages` *`list<message>`*: A filtered list of messages

- **POST**: Bulk create messages\
    <u>Data:</u>
    - `messages` *`list<new_message>`*: A list of messages to create

    <u>Returns:</u>
    - `message_ids` *`list<int>`*: The IDs of the newly created messages

- **DELETE**: Delete messages\
    <u>Data:</u>
    - [`message_ids` *`list<int>`*]: The IDs of the messages to retrieve. If not provided, all messages will be retrieved.\
    **OR**
    - [`filters` *`list<message_filter>`*]: A list of filters to apply to the messages. The results returned by each filter are joined with `OR`. If not provided, all messages will be retrieved.

    <u>Returns:</u>
    - `message_ids` *`list<int>`*: The IDs of the deleted messages

## Users

#### `user` data type:
- `user_id` *`int`*: The ID of the user
- `name` *`string`*: The name of the user
- `email` *`string`*: The email of the user
- `active` *`bool`*: Whether the user is active

#### `new_user` data type:
- `name` *`string`*: The name of the user
- `email` *`string`*: The email of the user
- `active` *`bool`*: Whether the user is active

#### `user_filter` data type:
- ['convo_ids' *`list<int>`*]: A list of conversation IDs to retrieve users from. Results are joined with `filter_mode`. If not provided, users from all conversations are retrieved.
- ['filter_mode' *`string`*]: The join mode for the above filter. Can be `'AND'` or `'OR'`. If not provided, OR is used.

### `/user`

- **POST**: Create a new user\
    <u>Data:</u>
    - `name` *`string`*: The name of the user
    - `email` *`string`*: The email of the user
    - `active` *`bool`*: Whether the user is active

    <u>Returns:</u>
    - `user_id` *`int`*: The ID of the newly created user

### `/user/<user_id:int>`
- **GET**: Retrieve info about the given user\
    <u>Returns:</u>
    - `user_id` *`int`*: The ID of the user
    - `name` *`string`*: The name of the user
    - `email` *`string`*: The email of the user
    - `active` *`bool`*: Whether the user is active

- **PUT**: Update the user with the given ID\
    <u>Data:</u>
    - [`name` *`string`*]: The new name of the user. If not provided, the name will not be updated.
    - [`email` *`string`*]: The new email of the user. If not provided, the email will not be updated.
    - [`active` *`bool`*]: Whether the user is active. If not provided, the active status will not be updated.

- **DELETE**: Delete the user with the given ID

### `/users`

- **GET**: Bulk retrieve users\
    <u>Data:</u>
    - [`user_ids` *`list<int>`*]: The IDs of the users to retrieve. If not provided, all users will be retrieved.\
    **OR**
    - [`filters` *`list<user_filter>`*]: A list of filters to apply to the users. The results returned by each filter are joined with `OR`. If not provided, all users will be retrieved.

    <u>Returns:</u>
    - `users` *`list<user>`*: A filtered list of users

- **POST**: Bulk create users\
    <u>Data:</u>
    - `users` *`list<new_user>`*: A list of users to create

    <u>Returns:</u>
    - `user_ids` *`list<int>`*: The IDs of the newly created users

- **DELETE**: Delete users\
    <u>Data:</u>
    - [`user_ids` *`list<int>`*]: The IDs of the users to retrieve. If not provided, all users will be retrieved.\
    **OR**
    - [`filters` *`list<user_filter>`*]: A list of filters to apply to the users. The results returned by each filter are joined with `OR`. If not provided, all users will be retrieved.

    <u>Returns:</u>
    - `user_ids` *`list<int>`*: The IDs of the deleted users

## Conversations

#### `convo` data type:
- `convo_id` *`int`*: The ID of the conversation
- `name` *`string`*: The name of the conversation
- `user_ids` *`list<int>`*: The IDs of the users in the conversation

#### `new_convo` data type:
- `name` *`string`*: The name of the conversation
- `user_ids` *`list<int>`*: The IDs of the users in the conversation

#### `convo_filter` data type:
- ['user_ids' *`list<int>`*]: A list of user IDs to retrieve conversations from. Results are joined with `filter_mode`. If not provided, conversations with all users are retrieved.
- ['filter_mode' *`string`*]: The join mode for the above filter. Can be `'AND'` or `'OR'`. If not provided, OR is used.

### `/convo`

- **POST**: Create a new conversation\
    <u>Data:</u>
    - `name` *`string`*: The name of the conversation

    <u>Returns:</u>
    - `convo_id` *`int`*: The ID of the newly created conversation

### `/convo/<convo_id:int>`

- **GET**: Retrieve info about the given conversation\
    <u>Returns:</u>
    - `convo_id` *`int`*: The ID of the conversation
    - `name` *`string`*: The name of the conversation

- **PUT**: Update the conversation with the given ID\
    <u>Data:</u>
    - [`name` *`string`*]: The new name of the conversation. If not provided, the name will not be updated.

- **DELETE**: Delete the conversation with the given ID

### `/convos`

- **GET**: Bulk retrieve conversations\
    <u>Data:</u>
    - [`convo_ids` *`list<int>`*]: The IDs of the conversations to retrieve. If not provided, all conversations will be retrieved.\
    **OR**
    - [`filters` *`list<convo_filter>`*]: A list of filters to apply to the conversations. The results returned by each filter are joined with `OR`. If not provided, all conversations will be retrieved.

    <u>Returns:</u>
    - `convos` *`list<convo>`*: A filtered list of conversations

- **POST**: Bulk create conversations\
    <u>Data:</u>
    - `convos` *`list<new_convo>`*: A list of conversations to create

    <u>Returns:</u>
    - `convo_ids` *`list<int>`*: The IDs of the newly created conversations

- **DELETE**: Delete conversations\
    <u>Data:</u>
    - [`convo_ids` *`list<int>`*]: The IDs of the conversations to retrieve. If not provided, all conversations will be retrieved.\
    **OR**
    - [`filters` *`list<convo_filter>`*]: A list of filters to apply to the conversations. The results returned by each filter are joined with `OR`. If not provided, all conversations will be retrieved.

    <u>Returns:</u>
    - `convo_ids` *`list<int>`*: The IDs of the deleted conversations

## Conversation Users

### `/convo/<convo_id:int>/user/<user_id:int>`
- **POST**: Add a user to a conversation

- **DELETE**: Remove a user from a conversation

### `/convo/<convo_id:int>/users`

- **GET**: Bulk retrieve users in a conversation\
    <u>Data:</u>
    - [`user_ids` *`list<int>`*]: The IDs of the users to retrieve. If not provided, all users will be retrieved.\
    **OR**
    - [`filters` *`list<user_filter>`*]: A list of filters to apply to the users. The results returned by each filter are joined with `OR`. If not provided, all users will be retrieved.

    <u>Returns:</u>
    - `users` *`list<user>`*: A filtered list of users

- **POST**: Bulk add users to a conversation\
    <u>Data:</u>
    - `user_ids` *`list<int>`*: The IDs of the users to add
    **OR**
    - [`filters` *`list<user_filter>`*]: A list of filters to apply to the users. The results returned by each filter are joined with `OR`. If not provided, all users will be added.

    <u>Returns:</u>
    - `user_ids` *`list<int>`*: The IDs of the users added

- **DELETE**: Bulk remove users from a conversation\
    <u>Data:</u>
    - `user_ids` *`list<int>`*: The IDs of the users to remove
    **OR**
    - [`filters` *`list<user_filter>`*]: A list of filters to apply to the users. The results returned by each filter are joined with `OR`. If not provided, all users will be removed.

    <u>Returns:</u>
    - `user_ids` *`list<int>`*: The IDs of the users removed