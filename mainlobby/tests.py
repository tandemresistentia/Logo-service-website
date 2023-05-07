from django.test import TestCase
from unittest.mock import patch, Mock
from django.urls import reverse
from django.conf import settings
import stripe
from .views import create_checkout_session

class TestCreateCheckoutSession(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('create_checkout_session')
        cls.product_id = 'product_regular'
        cls.quantity = 1
        cls.mock_stripe_session_id = 'mock_stripe_session_id'
        cls.mock_checkout_session = {'id': cls.mock_stripe_session_id}
        cls.mock_stripe_customer_id = 'mock_stripe_customer_id'
        cls.mock_stripe_checkout_session = Mock()
        cls.mock_stripe_checkout_session.id = cls.mock_stripe_session_id
        cls.mock_stripe_customer = Mock()
        cls.mock_stripe_customer.id = cls.mock_stripe_customer_id

    def setUp(self):
        self.request = self.client.post(self.url, {
            'product_id': self.product_id,
            'quantity': self.quantity,
        })

    @patch('stripe.checkout.Session.create', return_value=mock_checkout_session)
    @patch('stripe.Customer.create', return_value=mock_stripe_customer)
    def test_create_checkout_session(self, mock_customer_create, mock_session_create):
        response = create_checkout_session(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/orders/checkout/{self.mock_stripe_session_id}/')
        mock_session_create.assert_called_once_with(
            customer=self.mock_stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': PRODUCTS_STRIPE_PRICING_ID[self.product_id],
                'quantity': self.quantity,
            }],
            mode='payment',
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
        )
        mock_customer_create.assert_called_once_with(
            email=self.request.user.email,
        )