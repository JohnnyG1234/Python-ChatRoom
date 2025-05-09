import socket
import json
import threading
import sys

from helperfunctions import recv_message, send_message
HOST = 'localhost'  # IP of server
WRITING_PORT = 7778         # Port of server
READING_PORT = 7779

BROADCAST = "BROADCAST"
PRIVATE = "PRIVATE"
EXIT = "EXIT"
ERROR = 'Message format error'


class ChatClient:
    """This class will allow a client to message the server"""

    sending_sock = socket.socket()
    receiving_socket = socket.socket()
    screen_name = ""
    is_connected = False

    def __init__(self, screen_name=None):
        """This fucntion will make an instance of a client

        it will make a reciving socka and a sending sock and start a thread
        for each of them to do their thing
        """

        if not screen_name:
            self.get_screen_name()
        else:
            self.screen_name = screen_name
            
        self.receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sending_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.is_connected = ChatClient.connect(self.receiving_socket, HOST, WRITING_PORT) and ChatClient.connect(self.sending_sock, HOST, READING_PORT)

        if not self.is_connected:
            print("failed to connect to server")
            return

        threading.Thread(target=self.receiving, args=()).start()
        threading.Thread(target=self.sending, args=()).start()

    def sending(self):
        """This handles sending messages to the server"""

        while True:
            message_input = input("> ")
            list = []

            if not message_input:
                print("No message")
                continue

            if message_input[0] == '@':
                self.private_msg(message_input)

            elif message_input == "Exit" or message_input == "exit":
                self.exit()
                return
            else:
                self.broadcast_msg(message_input)


    def receiving(self):
        """This will handle receiving starting a connection with the server

        It will also handle receiving messages from the server
        and printing those messages to the screen
        """

        start_msg = ["START", self.screen_name]
        send_message(self.receiving_socket, start_msg)

        while True:
            message = recv_message(self.receiving_socket)
            if (message == "Closing"):
                print(message)
                return
            print(message)

    def get_screen_name(self):
        """This will get a proper screen name from the client"""

        self.screen_name = input("Please enter your desired screen name: ")

        while not self.check_screen_name(self.screen_name):
            self.screen_name = input("Invalid screen name, please try again: ")

        print("screen name accepted")

    def check_screen_name(self, screen_name):
        """This checks if a given screen name is valid"""
        # TODO: Make  sure no other users  have  the same screen name
        for c in screen_name:
            if c == " ":
                return False

        if not screen_name:
            return False
        
        return  True
    
    def private_msg(self, message_input):
        """Sends a private message request to the server, makes sure there is a message and a username before sending"""
        name = message_input.split(" ", 1)
        screen_name = name[0]
        try:
            message_input = name[1]
        except IndexError:
            print("No message")
            return
        screen_name = screen_name[1:]
        list = [PRIVATE, self.screen_name, message_input, screen_name]

        send_message(self.sending_sock, list)
    
    def exit(self):
        """Tells the server the client is leaving"""
        list = [EXIT, self.screen_name]
        send_message(self.sending_sock, list)
        self.is_connected = False
    
    def broadcast_msg(self, message_input):
        """sends a message to all other users"""
        list = [BROADCAST, self.screen_name, message_input]

        send_message(self.sending_sock, list)


    @staticmethod
    def connect(sock, host, port) -> bool:
        """Connects a socket to another socket, returns true on success and False on a failure"""
        try:
            sock.connect((host, port))
        except Exception as e:
            print("Connection failed:", e)
            return False
        else:
            print("Connection established to writing port")
            return True


if __name__ == '__main__':
    client = ChatClient()