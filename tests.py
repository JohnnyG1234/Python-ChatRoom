import unittest
import client
import server

class TestScreenName(unittest.TestCase):
    def test_invalid_name_1(self):
        test_server = server.ChatServer()
        test_client = client.ChatClient("test")
        self.assertFalse(test_client.check_screen_name("Jimmy Dean"))
        test_server.shutdown()
        
    def test_invalid_name_2(self):
        test_server = server.ChatServer()
        test_client = client.ChatClient("test")
        self.assertFalse(test_client.check_screen_name(""))
        test_server.shutdown()
    
    def test_valid_name_1(self):
        test_server = server.ChatServer()
        test_client = client.ChatClient("test")
        self.assertTrue(test_client.check_screen_name("Jimmy_Dean"))
        test_server.shutdown()
    
    def test_valid_name_2(self):
        test_server = server.ChatServer()
        test_client = client.ChatClient("test")
        self.assertTrue(test_client.check_screen_name("XX_K3WLDUD3_XX"))
        test_server.shutdown()

if __name__ == '__main__':
    unittest.main()