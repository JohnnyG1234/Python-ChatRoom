import socket
import json


def recv_all(length, client_sock):
        """this function receives the amount of data given"""
        ERROR = 'Message format error'
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

def  recv_message(client_sock):
        length_bytes = client_sock.recv(4)
        length = int.from_bytes(length_bytes, "big")
        data = recv_all(length, client_sock)
        data_decoded = data.decode('utf-8')
        return json.loads(data_decoded)