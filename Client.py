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
            
        self.receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.receiving_socket.connect((HOST, WRITING_PORT))
        except Exception as e:
            print("Connection failed:", e)
            self.is_connected = False
        else:
            self.is_connected = True
            print("Connection established to writing port")


        self.sending_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sending_sock.connect((HOST, READING_PORT))
        except Exception as e:
            self.is_connected = False
            print("Connection failed:", e)
        else:
            self.is_connected = True
            print("Connection established to reading port.")

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
                name = message_input.split(" ", 1)
                screen_name = name[0]
                try:
                    message_input = name[1]
                except IndexError:
                    print("No message")
                    continue
                screen_name = screen_name[1:]
                list = [PRIVATE, self.screen_name, message_input, screen_name]

                json_list = json.dumps(list)
                encoded = json_list.encode('utf-8')

                size = len(encoded)
                byte_size = size.to_bytes(4, 'big')
                message = byte_size + encoded
                self.sending_sock.sendall(message)

            elif message_input == "Exit" or message_input == "exit":
                list = [EXIT, self.screen_name]

                json_list = json.dumps(list)
                encoded = json_list.encode('utf-8')

                size = len(encoded)
                byte_size = size.to_bytes(4, 'big')
                message = byte_size + encoded
                self.sending_sock.sendall(message)
                return
            else:
                list = [BROADCAST, self.screen_name, message_input]

                json_list = json.dumps(list)
                encoded = json_list.encode('utf-8')

                size = len(encoded)
                byte_size = size.to_bytes(4, 'big')
                message = byte_size + encoded
                self.sending_sock.sendall(message)


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

        for c in screen_name:
            if c == " ":
                return False

        if not screen_name:
            return False
        
        return  True

    def unpack_message(self, message):
        """This will decode and make a json message into a python object"""

        message_decoded = message.decode('utf-8')
        message_loads = json.loads(message_decoded)
        return message_loads

    def recv_all(self, length, client_sock):
        """this function receives the amount of data given"""

        data = b''
        while len(data) < length:
            more = client_sock.recv(length - len(data))
            if not more:
                return_length = len(ERROR.encode("utf-8"))
                error_message = return_length.to_bytes(4, "big") + ERROR.encode("utf-8")
                client_sock.sendall(error_message)
                raise EOFError
            data += more
        return data


if __name__ == '__main__':
    client = ChatClient()