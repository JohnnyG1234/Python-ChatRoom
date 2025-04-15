import unittest
import client
import server

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
    def test_connection(self):
        self.assertTrue(test_client.is_connected)

if __name__ == '__main__':
    unittest.main()