import unittest
import Client
import server

class TestScreenName(unittest.TestCase):
    def test_invalid_name_1(self):
        client = Client.ChatClient(ifTesting=True)
        self.assertFalse(client.check_screen_name("Jimmy Dean"))

    def test_invalid_name_2(self):
        client = Client.ChatClient(ifTesting=True)
        self.assertFalse(client.check_screen_name(""))
    
    def test_valid_name_1(self):
        client = Client.ChatClient(ifTesting=True)
        self.assertTrue(client.check_screen_name("Jimmy_Dean"))
    
    def test_valid_name_2(self):
        client = Client.ChatClient(ifTesting=True)
        self.assertTrue(client.check_screen_name("XX_K3WLDUD3_XX"))

if __name__ == '__main__':
    unittest.main()