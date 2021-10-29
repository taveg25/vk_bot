#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from _token import token
import random
import vk_api
import vk_api.bot_longpoll

group_id = 41621661


class Bot(object):
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()



    def run(self):
        for event in self.long_poller.listen():
            # print('Send a message')
            try:
                self.on_event(event)
            except Exception as exc:
                print(exc)

    def on_event(self, event):
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            print(event.object.message['text'])
            self.api.messages.send(message=f'было полученно сообщение: '
                                           f"{event.object.message['text']}",
                                   random_id=random.randint(0, 2 ** 20),
                                   peer_id=event.object.message['peer_id'])
        else:
            print('Мы пока не умеем обрабатывать события такого типа', event.type)


if __name__ == "__main__":
    bot = Bot(group_id, token)
    bot.run()