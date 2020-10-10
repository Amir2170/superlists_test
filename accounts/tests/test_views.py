from django.test import TestCase
from unittest.mock import patch

import accounts.views


class SendLoginEmailViewTest(TestCase):
    
    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'mysuperlists2170@gmail.com'
            })
        self.assertRedirects(response, '/')
    
    @patch('accounts.views.send_mail')
    def test_send_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={
            'email': 'amirrezaamp2170@gmail.com'
            })
        
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs= mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'amirrezaamp2170@gmail.com')
        self.assertEqual(to_list, ['mysuperlists2170@gmail.com'])
1
