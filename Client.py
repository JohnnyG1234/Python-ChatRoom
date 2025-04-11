import socket
import json
import threading
import sys

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

    def __init__(self, ifTesting=False):
        """This fucntion will make an instance of a client

        it will make a reciving socka and a sending sock and start a thread
        for each of them to do their thing
        """

        if ifTesting:
            return

        self.get_screen_name()

        self.receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiving_socket.connect((HOST, WRITING_PORT))

        self.sending_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sending_sock.connect((HOST, READING_PORT))

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

        start = ["START", self.screen_name]
        json_start = json.dumps(start)
        encoded = json_start.encode('utf-8')

        size = len(encoded)
        size_bytes = size.to_bytes(4, 'big')
        message = size_bytes + encoded

        self.receiving_socket.sendall(message)

        while True:

            byte_size = self.receiving_socket.recv(4)
            length = int.from_bytes(byte_size, "big")

            data = self.recv_all(length, self.receiving_socket)
            message = self.unpack_message(data)
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