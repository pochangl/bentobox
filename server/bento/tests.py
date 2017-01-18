from django.test import TestCase, Client
from .models import Order
import json


class OrderTest(TestCase):
    client = Client()
    orders = [
        {'id': 'd123456781', 'resNo': '#1', 'vegetarianBox': 1, 'ribsBox': 5, 'vat': '123345'},
    ]

    def get_identifier(self, order):
        return {'id': order['id'], 'resNo': order['resNo']}

    def orderEqual(self, instance, order):
        for key, value in order.items():
            self.assertEqual(getattr(instance, key), value)

    def test_without_captcha(self):
        order = self.orders[0]
        identifier = self.get_identifier(order)
        response = self.client.post('/order', order)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_flow(self):
        order = self.orders[0]
        identifier = self.get_identifier(order)
        captchaed_order = order.copy()

        self.client.get('/captcha')
        response = self.client.get('/current_captcha')
        captchaed_order['captcha'] = response.content.decode('utf-8')

        response = self.client.post('/order', captchaed_order)

        instance = Order.objects.get()
        self.orderEqual(instance, order)
        self.assertIsNotNone(instance.created_at)

        order['vegetarianBox'] = 2
        order['ribsBox'] = 3
        response = self.client.post('/update', order)

        instance = Order.objects.get()
        self.orderEqual(instance, order)

        response = self.client.post('/query', identifier)
        self.assertJSONEqual(response.content.decode('utf-8'), order)

        response = self.client.post('/cancel', identifier)

        self.assertEqual(Order.objects.count(), 0)
