import socket
import json


def recv_all(length, sock):
        """this function receives the amount of data given"""
        ERROR = 'Message format error'
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                return_length = len(ERROR.encode("utf-8"))
                error_message = return_length.to_bytes(4, "big") + ERROR.encode("utf-8")
                sock.sendall(error_message)
                raise EOFError
            data += more
        return data

def  recv_message(sock):
        """Recv a message on a given socket and returns a python string"""
        length_bytes = sock.recv(4)
        length = int.from_bytes(length_bytes, "big")
        data = recv_all(length, sock)
        data_decoded = data.decode('utf-8')
        return json.loads(data_decoded)

def  send_message(sock, msg):
      """Sends a properly encoded/formated message based off given msg"""
      json_msg = json.dumps(msg)

      encoded = json_msg.encode('utf-8')

      size = len(encoded)
      size_bytes = size.to_bytes(4, 'big')
      message = size_bytes + encoded
      
      sock.sendall(message)


      