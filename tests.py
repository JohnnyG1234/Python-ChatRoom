import unittest
import client
import server

class TestScreenName(unittest.TestCase):
    test_server = server.ChatServer()
    test_client = client.ChatClient("test1")

    def test_invalid_name_1(self):
        self.assertFalse(self.test_client.check_screen_name("Jimmy Dean"))
        
    def test_invalid_name_2(self):
        self.assertFalse(self.test_client.check_screen_name(""))
    
    def test_valid_name_1(self):
        self.assertTrue(self.test_client.check_screen_name("Jimmy_Dean"))
    
    def test_valid_name_2(self):
        self.assertTrue(self.test_client.check_screen_name("XX_K3WLDUD3_XX"))

if __name__ == '__main__':
    unittest.main()