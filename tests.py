import unittest
from copy import deepcopy
from unittest.mock import patch, Mock, ANY

from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent

import settings
from bot import Bot
from generate_ticket import generate_ticket


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()
    return wrapper



class Test1(unittest.TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {'message':
             {'date': 1635827333, 'from_id': 48579187, 'id': 64, 'out': 0, 'peer_id': 48579187,
              'text': 'й', 'conversation_message_id': 62, 'fwd_messages': [], 'important': False,
              'random_id': 0, 'attachments': [], 'is_hidden': False},
                   'client_info':
            {'button_actions': ['text', 'vkpay', 'open_app', 'location',
                                'open_link', 'callback', 'intent_subscribe', 'intent_unsubscribe'],
             'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}},
                 'group_id': 41621661, 'event_id': 'b4219a8adefedd28643ed50a60a52226fe0ad846'}

#     def test_run(self):
#         count = 5
#         obj = {'a': 1}
#         events = [obj] * count
#         long_poller_mock = Mock(return_value=events)
#         long_poller_listen_mock = Mock()
#         long_poller_listen_mock.listen = long_poller_mock
#         with patch('bot.vk_api.VkApi'):
#             with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
#                 bot = Bot('','')
#                 bot.on_event = Mock()
#                 bot.run()
#
#                 bot.on_event.assert_called()
#                 bot.on_event.assert_any_call(obj)
#                 assert bot.on_event.call_count == count
#
#     INPUTS = [
#         'Привет',
#         'А когда?',
#         'Где будет конференция?',
#         'Зарегистрируй меня',
#         'Веня',
#         'мой адрес email@email',
#         'email@email.ru',
#     ]
#     EXPECTED_OUTPUTS = [
#         settings.DEFAULT_ANSWER,
#         settings.INTENTS[0]['answer'],
#         settings.INTENTS[1]['answer'],
#         settings.SCENARIOS['registration']['steps']['step1']['text'],
#         settings.SCENARIOS['registration']['steps']['step2']['text'],
#         settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
#         settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Веня', email='email@email.ru'),
#     ]
#
#     @isolate_db
#     def test_run_ok(self):
#         send_mock = Mock()
#         api_mock = Mock()
#         api_mock.messages.send = send_mock
#
#         events = []
#         for input_text in self.INPUTS:
#             event = deepcopy(self.RAW_EVENT)
#             event['object']['text'] = input_text
#             events.append(VkBotMessageEvent(event))
#
#         long_poller_mock = Mock()
#         long_poller_mock.listen = Mock(return_value=events)
#
#         with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
#             bot = Bot('','')
#             bot.api = api_mock
#             bot.run()
#
#         assert send_mock.call_count == len(self.INPUTS)
#
#         real_outputs = []
#         for call in send_mock.call_args_list:
#             args, kwargs = call
#             real_outputs.append(kwargs['message'])
#         assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        with open('files/email.png', 'rb') as avatar_file:
            avatar_mock = Mock()
            avatar_mock.content = avatar_file.read()
        with patch('requests.get', return_value=avatar_mock):
            ticket_file = generate_ticket('nanjj', 'email')

        with open('files/ticket_example.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()
        assert ticket_file.read() == expected_bytes


if __name__ == '__main__':
    unittest.main()