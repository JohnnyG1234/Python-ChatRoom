import json
import socket
import threading

from helperfunctions import recv_message, send_message

HOST = 'localhost'  # IP of server
WRITING_PORT = 7778
READING_PORT = 7779
ERROR = 'Message format error'
USER_JOINED = ' has joined the chat'


class ChatServer:
    """This server will hold a list of clients and send messages back and forht between them"""

    reading_sock = socket.socket()
    writing_sock = socket.socket()
    client_list = [] # List of tuples each client is a tuple client[0] == username client[1] == socket associated with that client
    _should_run = True

    def __init__(self):
        """This funciton will make an instance of the server

        it will make a reading sock and a writing sock as well as create
        threads to handle both of those socks
        """

        self.reading_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.writing_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        if not ChatServer.bind(self.reading_sock, HOST, READING_PORT)  or not ChatServer.bind(self.writing_sock, HOST, WRITING_PORT):
            print("Failed to bind")
            return
        

        threading.Thread(target=self.writing, args=()).start()
        threading.Thread(target=self.reading, args=()).start()

        print(f'Server running at {HOST}')

    def reading(self):
        """this function will start a new thread after reciving a connection"""

        while self._should_run:
            client_sock, address = self.reading_sock.accept()
            threading.Thread(target=self.handle_chat, args=(client_sock,)).start()

        self.reading_sock.close()

    def handle_chat(self, client_sock):
        """This will handle a chat from one client

        it will take the input from the client and take the corresponding action
        according to the message it got
        """

        while self._should_run:
            """
            message[0] = message type 
            message[1] = username
            message[2] = message content
            """
            try:
                message = recv_message(client_sock) 
            except:
                print("Client closed connection")
                break

            if message[0] == "BROADCAST":
                self.broadcast(message)

            elif message[0] == "EXIT":
                self.exit(client_sock, message)
                break

            elif message[0] == "PRIVATE":
                self.private_message(message)

        client_sock.close()

    def writing(self):
        """This will acepts new connections from clients and send out a welcome message"""

        while self._should_run:
            client_sock, address = self.writing_sock.accept()

            message = recv_message(client_sock)
            self.client_list.append((message[1], client_sock))
            send_back = message[1] + USER_JOINED
            
            for clients in self.client_list:
                send_message(clients[1], send_back)
                
        self.writing_sock.close()

    
    def shutdown(self):
        """Stops all sockets from running"""
        self._should_run = False

    def broadcast(self, message):
        """Sends a message to all clients"""
        username = message[1]
        msg = message[2]

        send_back = username + ": " + msg

        for clients in self.client_list:
            send_message(clients[1], send_back)
    
    def exit(self, sock, message):
        """Lets one client exit the program"""
        username = message[1]
        
        sock.close()
        client_to_close = self.find_client(username)[1]
        send_message(client_to_close, "Closing")
    
    def private_message(self, message):
        """Sends a private message to specified username"""
        username = message[1]
        msg = message[2]

        target_username = message[3]
        target_client = self.find_client(target_username)[1]

        send_back = username + " (private): " + msg
        send_message(target_client, send_back)

    def find_client(self, username): # returns a client
        for client in self.client_list:
            if client[0] == username:
                return client
        return None
    
    def get_all_usernames(self):
        usernames = []
        for client in self.client_list:
            usernames.append(client[0])
        
        return usernames

    @staticmethod
    def bind(sock, host, port) -> bool:
        """binds a sock to a host and port and gets ready for connections, returns bool representing if bind was succesfull"""
        try:
            sock.bind((host, port))
            sock.listen()
        except socket.error as e:
            return False

        return True
                



if __name__ == '__main__':
    server = ChatServer()

