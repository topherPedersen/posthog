from django.test import TestCase, Client

class TestSignup(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
     
    def test_ip_range(self):
        with self.settings(ALLOWED_IP_BLOCKS='192.168.0.0/31, 127.0.0.0/25,128.0.0.1'):
            # not in list
            response = self.client.get('/', REMOTE_ADDR='10.0.0.1')
            self.assertIn(b'IP is not allowed', response.content)

            response = self.client.get('/batch/', REMOTE_ADDR='10.0.0.1')
            self.assertEqual(b'1', response.content)

            # /31 block
            response = self.client.get('/', REMOTE_ADDR='192.168.0.1')
            self.assertNotIn(b'IP is not allowed', response.content)

            response = self.client.get('/', REMOTE_ADDR='192.168.0.2')
            self.assertIn(b'IP is not allowed', response.content)

            response = self.client.get('/batch/', REMOTE_ADDR='192.168.0.1')
            self.assertEqual(b'1', response.content)

            response = self.client.get('/batch/', REMOTE_ADDR='192.168.0.2')
            self.assertEqual(b'1', response.content)

            # /24 block
            response = self.client.get('/', REMOTE_ADDR='127.0.0.1')
            self.assertNotIn(b'IP is not allowed', response.content)

            response = self.client.get('/', REMOTE_ADDR='127.0.0.100')
            self.assertNotIn(b'IP is not allowed', response.content)

            response = self.client.get('/', REMOTE_ADDR='127.0.0.200')
            self.assertIn(b'IP is not allowed', response.content)

            # precise ip
            response = self.client.get('/', REMOTE_ADDR='128.0.0.1')
            self.assertNotIn(b'IP is not allowed', response.content)

            response = self.client.get('/', REMOTE_ADDR='128.0.0.2')
            self.assertIn(b'IP is not allowed', response.content)