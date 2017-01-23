from django.test import TestCase, Client
from .models import Order
import json


class OrderTest(TestCase):
    client = Client()
    orders = [
        {'id': 'd123456781', 'resNo': '1', 'vegetarianBox': 1, 'ribsBox': 5, 'vat': '123345'},
    ]

    def get_identifier(self, order):
        return {'id': order['id'], 'resNo': order['resNo']}

    def orderEqual(self, instance, order):
        for key, value in order.items():
            self.assertEqual(getattr(instance, key), value)

    def test_without_captcha(self):
        order = self.orders[0]
        identifier = self.get_identifier(order)
        response = self.client.post('/api/order', order)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_flow(self):
        order = self.orders[0]
        identifier = self.get_identifier(order)
        captchaed_order = order.copy()

        self.client.get('/api/captcha')
        response = self.client.get('/api/current_captcha')
        captchaed_order['captcha'] = response.content.decode('utf-8')

        response = self.client.post('/api/create_order', captchaed_order)
        print (response.status_code, response.content)

        instance = Order.objects.get()
        self.orderEqual(instance, order)
        self.assertIsNotNone(instance.created_at)

        order['vegetarianBox'] = 2
        order['ribsBox'] = 3
        response = self.client.put('/api/order/%(resNo)s/%(id)s' % order, json.dumps(order), content_type='application/json')
        print (order)
        print ('/api/order/%(resNo)s/%(id)s' % order)
        print (response.status_code, response.content)

        instance = Order.objects.get()
        self.orderEqual(instance, order)

        response = self.client.get('/api/order/%(resNo)s/%(id)s' % order, identifier)
        self.assertJSONEqual(response.content.decode('utf-8'), order)

        response = self.client.delete('/api/order/%(resNo)s/%(id)s' % order, identifier)

        self.assertEqual(Order.objects.count(), 0)
