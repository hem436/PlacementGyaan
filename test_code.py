import unittest
import requests

class Test(unittest.TestCase):
    
    def test_login(self):
        request=requests.Session().post('http://127.0.0.1:8080/login',data={'name':'user', 'password':'password'})
        self.assertEqual(request.status_code,500)
    def test_signup(self):
        request=requests.Session().post('http://127.0.0.1:8080/signup',data={'name':'user', 'password':'password'})
        self.assertEqual(request.status_code,200)