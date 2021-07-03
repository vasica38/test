import unittest
from random import random
import random, string

import main

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


class ControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = main.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.payload = {'name': randomword(5)}

    def test_get_response(self):
        response = self.client.post('/workers', json=self.payload)
        expected_resp = {'name' : self.payload['name']}
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/workers', json=self.payload)
        expected_resp = {'name' : self.payload['name']}
        self.assertEqual(response.status_code, 400)

    def test_add_shift_response(self):
        #try to add a shift
        response = self.client.post('/workers', json=self.payload)
        response = self.client.post('/shifts', json={
                "date" : "18/08/20 08:00:00",
                "worker_name" : self.payload['name']
         })
        self.assertEqual(response.status_code, 200)


        #try to add second shift same day but different
        response = self.client.post('/shifts', json={
                "date" : "18/08/20 16:00:00",
                "worker_name" : self.payload['name']
         })
        self.assertEqual(response.status_code, 400)

        #try to add a shift with wrong  worker name
        response = self.client.post('/shifts', json={
                "date" : "18/08/20 08:00:00",
                "worker_name" : 'wrong name'
         })
        self.assertEqual(response.status_code, 400)

    def test_get_workers(self):
        response = self.client.get('/workers')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
