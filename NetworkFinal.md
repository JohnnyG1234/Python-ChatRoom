To run the program simply run the server first, then run as many clients as you want



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



Additional info:

- The server has two ports both under the "localhost" host name
- The writing port is 7778, and the reading port is 7779
- Private messages with no content (for example if input == "") will not be accepted as that causes an exception
- Broadcast with no message is ok though
- Network programming is pretty cool