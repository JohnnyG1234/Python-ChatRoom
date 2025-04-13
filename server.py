import json
import socket
import threading

HOST = 'localhost'  # IP of server
WRITING_PORT = 7778
READING_PORT = 7779
ERROR = 'Message format error'
USER_JOINED = ' has joined the chat'


class ChatServer:
    """This server will hold a list of clients and send messages back and forht between them"""

    reading_sock = socket.socket()
    writing_sock = socket.socket()
    client_list = []
    _should_run = True

    def __init__(self):
        """This funciton will make an instance of the server

        it will make a reading sock and a writing sock as well as create
        threads to handle both of those socks
        """

        self.reading_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reading_sock.bind((HOST, READING_PORT))
        self.reading_sock.listen()

        self.writing_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.writing_sock.bind((HOST, WRITING_PORT))
        self.writing_sock.listen()

        threading.Thread(target=self.writing, args=()).start()
        threading.Thread(target=self.reading, args=()).start()

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
            length_bytes = client_sock.recv(4)
            length = int.from_bytes(length_bytes, "big")
            data = self.recv_all(length, client_sock)
            data_decoded = data.decode('utf-8')
            message = json.loads(data_decoded)

            if message[0] == "BROADCAST":
                send_back = message[1] + ": " + message[2]
                json_back = json.dumps(send_back)
                encoded = json_back.encode('utf-8')

                length = len(encoded)
                length_bytes = length.to_bytes(4, 'big')
                final = length_bytes + encoded

                for clients in self.client_list:
                    clients[1].sendall(final)
            elif message[0] == "EXIT":
                send_back = "Closing"
                json_back = json.dumps(send_back)
                encoded = json_back.encode('utf-8')

                length = len(encoded)
                length_bytes = length.to_bytes(4, 'big')
                final = length_bytes + encoded
                client_sock.close()
                for clients in self.client_list:
                    if clients[0] == message[1]:
                        clients[1].sendall(final)
                        break
                return
            elif message[0] == "PRIVATE":
                send_back = message[1] + " (private): " + message[2]
                json_back = json.dumps(send_back)
                encoded = json_back.encode('utf-8')

                length = len(encoded)
                length_bytes = length.to_bytes(4, 'big')
                final = length_bytes + encoded

                for clients in self.client_list:
                    if clients[0] == message[3]:
                        clients[1].sendall(final)
                        break

        client_sock.close()

    def writing(self):
        """This will acepts new connections from clients and send out a welcome message"""

        while self._should_run:
            client_sock, address = self.writing_sock.accept()

            length_bytes = client_sock.recv(4)
            length = int.from_bytes(length_bytes, "big")
            data = self.recv_all(length, client_sock)

            data_decoded = data.decode()
            message = json.loads(data_decoded)
            self.client_list.append((message[1], client_sock))

            send_back = message[1] + USER_JOINED
            json_back = json.dumps(send_back)
            encoded_back = json_back.encode('utf-8')

            length = len(encoded_back)
            length_bytes = length.to_bytes(4, 'big')
            new_user_message = length_bytes + encoded_back
            
            for clients in self.client_list:
                clients[1].sendall(new_user_message)
                
        self.writing_sock.close()

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
    
    def shutdown(self):
        self._should_run = False


if __name__ == '__main__':
    server = ChatServer()

