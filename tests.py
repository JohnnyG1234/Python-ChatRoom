import unittest
import client
import server
import socket

test_server = server.ChatServer()
test_client = client.ChatClient("test")

class TestScreenName(unittest.TestCase):
    def test_invalid_name_1(self):
        self.assertFalse(test_client.check_screen_name("Jimmy Dean"))
        
    def test_invalid_name_2(self):
        self.assertFalse(test_client.check_screen_name(""))
    
    def test_valid_name_1(self):
        self.assertTrue(test_client.check_screen_name("Jimmy_Dean"))
    
    def test_valid_name_2(self):
        self.assertTrue(test_client.check_screen_name("XX_K3WLDUD3_XX"))

class TestConnection(unittest.TestCase):
    def test_connection_1(self):
        self.assertTrue(test_client.is_connected)

    def test_connection_2(self):
        HOST = 'localhost'
        PORT = 1050
        test_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        test_server.bind(test_server_sock, 'localhost', 1050)
        self.assertTrue(test_client.connect(test_client_sock, HOST, PORT))

        test_client_sock.close()
        test_server_sock.close()

        

if __name__ == '__main__':
    unittest.main()