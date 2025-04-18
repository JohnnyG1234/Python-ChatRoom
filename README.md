To run the program simply run the server first, then run as many clients as you want

run the server with 

```
python server.py
```

run the client  with

```
python Client.py
```

and run tests with
```
python tests.py
```


You don't have to have any inputs on the server end

The client will first ask for a screen name, it will not except screen names with spaces in them, or blank screen names



The client will then wait for input to send to the server

- Broadcast messages can simply be entered with nothing else (just type a message when you see the >)
- Private messages must be formatted like this `@Screen_name message`
- Exit messages will be send if the input is "Exit" or "exit" this will shut down both client threads



Here is an example run from the clients perspective

1. First the client will be asked for a screen name

   `Please enter your desired screen name: John`
   `screen name accepted`

   `John has joined the chat`

2. Next John will send a message in broadcast mode

   `Hello World`

   `John:  Hello World`

3. John can also send a private message, and because he is lonely and has no friends he sends one to himself

   `@John Hey buddy`

   `John (private): Hey buddy`

4. Finally John can send the exit message to quit the program

   `exit`
   `Closing`

   `Process finished with exit code 0`


The Protocol

The basic protocol that this program will follow is sending UTF-8 encoded JSON messages over TCP sockets prefixed by the message length (complete length of JSON message) encoded as 4 byte unsigned integers


    START: This message announces the connection of a chat client to the server. It will include the screen name of the client who is joining.
    BROADCAST: This message contains text that should be sent to every client connected to the chat server. It will include the screen name of the sender and the text of the message.
    PRIVATE: This message contains text that should be sent only to a single client connected to the chat server. It will include the screen name of the sender, the screen name of the intended recipient, and the text of the message.
    EXIT: This message announces the disconnection of a chat client from the server. It will include the screen name of the client who is leaving.
