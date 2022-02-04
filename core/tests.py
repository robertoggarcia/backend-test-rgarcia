from unittest import mock

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase, Client, RequestFactory
from slack_sdk.errors import SlackApiError

from core.management.commands.default_users import Command
from core.slack import send_slack_message


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        command = Command()
        command.handle()

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', password='Test', email='user@gmail.com'
        )
        self.chef = User.objects.get(username='chef')
        self.employee = User.objects.get(username='employee')


class SlackTest(BaseTest):

    @mock.patch('core.slack.WebClient.chat_postMessage')
    def test_send_message(self, m_request):
        site = Site.objects.get_current()
        url = f'https://{site.domain}/menu/id-testing/'
        message = f"Hello! I share today's menu : {url}"
        m_request.return_value = {
            "message": {"text": message}
        }

        result = send_slack_message('id-testing')

        self.assertEqual(message, result)

    @mock.patch('core.slack.WebClient.chat_postMessage')
    def test_send_message_fail(self, m_request):

        m_request.side_effect = SlackApiError('Error', {
            "ok": False,
            "error": "Failed"
        })

        self.assertRaises(Exception, send_slack_message, 'id-testing')
