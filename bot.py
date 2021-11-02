#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import random
try:
    import settings
except ImportError:
    exit('Do cp settings.py.default settings.py and set TOKEN')
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType



log = logging.getLogger('bot')
def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


class Bot(object):
    """
    Echo bot for vk.com

    Use python3.7
    """
    def __init__(self, group_id, token):
        """
        :param group_id: group_id from group vk.com
        :param token: secret token from group vk.com

        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()



    def run(self):
        """
        Run bot
        """
        for event in self.long_poller.listen():
            # print('Send a message')
            try:
                self.on_event(event)
            except Exception as exc:
                log.exception('ошибка в обработке события')

    def on_event(self, event):
        """
        handle bots messages: sent our message back, if it's text
        :param event: VkBotMessageEvent object
        :return: None

        """

        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug('отправляем сообщение назад')
            self.api.messages.send(message=f'было полученно сообщение: '
                                           f"{event.object.message['text']}",
                                   random_id=random.randint(0, 2 ** 20),
                                   peer_id=event.object.message['peer_id'])
        else:
            log.info(f'Мы пока не умеем обрабатывать события такого типа {event.type}')


if __name__ == "__main__":
    configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()