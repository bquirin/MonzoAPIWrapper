import unittest 
from unittest.mock import patch 
from monzo_api_wrapper import MonzoClient

class TestMonzoAPIWrapper(unittest.TestCase):
    
    
    def setUp(self):
        access_token = ("eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJlYiI6InNtbW9ZQ2pwOXBVa2VWUkdGb1dnIiwianRpIj"
        "oiYWNjdG9rXzAwMDBBTHAzU2RHSFVTMWlvZE10ZnQiLCJ0eXAiOiJhdCIsInYiOiI2In0.hr_XuChcPvuyg5LlxyvprZDt2eRzN6gvf"
        "JSnIRh0oXC1VBZ10pipS0rlJWV33rOAMBjrGlzHX7v6t7RjWYKEyg")

        self.monzo = MonzoClient(access_token)

    
    def tearDown(self):
        return super().tearDown()

    
    def test_attributes(self):
        self.assertEqual(self.monzo.monzo_base_url, "https://api.monzo.com")

    def test_validate_acccess_token(self):
        with self.assertRaises(TypeError):
            self.monzo(10)  
        with self.assertRaises(ValueError):
            MonzoClient('addfd2dfdf.cdsfddfs')

    def test_make_request(self):
        with patch('monzo_api_wrapper.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            response = self.monzo.make_request("/ping/whoami")
            mocked_get.assert_called_with("https://api.monzo.com/ping/whoami")
            self.asserEqual(response, "Success")






if __name__ == '__main__':
    unittest.main()




