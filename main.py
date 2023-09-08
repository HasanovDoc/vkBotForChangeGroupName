import vk_api
import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import *

vk_session = vk_api.VkApi(token = main_token)
longpoll = VkBotLongPoll(vk_session, groupId)

flag = True

WEEKDAYNUM = 0


def changeName(id, text):
    vk_session.method('messages.editChat', {'chat_id': id, 'title': text})
    return False
    
def sendMessage(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'random_id': 0, 'message': text})

def getTitleChatName(id):
    req = vk_session.method('messages.getConversationsById', {"peer_ids": 2000000000 + id})#["title"]
    for response in req['items']:
        chat_settings = response['chat_settings']
        title = chat_settings['title']
    return title

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            msg = event.object.message['text'].lower()
            id = event.chat_id         
            #if msg == '/changename':
            titleChat = getTitleChatName(id)
            print(f'Номер дня: {datetime.datetime.today().weekday()}\nflag: {flag}')
            if datetime.datetime.today().weekday() == WEEKDAYNUM and flag:
                if titleChat.count('ЧИСЛИТЕЛЬ') == 1:
                    flag = changeName(id, titleChat.replace('ЧИСЛИТЕЛЬ', 'ЗНАМЕНАТЕЛЬ'))
                elif titleChat.count('ЗНАМЕНАТЕЛЬ') == 1:
                    flag = changeName(id, titleChat.replace('ЗНАМЕНАТЕЛЬ', 'ЧИСЛИТЕЛЬ'))

            if datetime.datetime.today().weekday() != WEEKDAYNUM:
                flag = True
            else:
                flag = False
            #sendMessage(id, f'{datetime.datetime.today().weekday()}, {id}')















# class MyLongPoll(VkBotLongPoll):
#     def listen(self):
#         while True:
#             try:
#                 for event in self.check():
#                     yield event
#             except Exception as e:
#                 print(e)
            
# class VkBot:
#     def __init__(self):
#         self.vk_session = vk_api.VkApi(token = main_token)
#         self.longpoll = MyLongPoll(self.vk_session, 222452856)
#         # self.vk_id = self.vk_session.get_user_id()
#         # self.vk_name = self.vk_session.get_user_name()
#         # self.vk_photo = self.vk_session.get_user_photo(self.vk_id)
#         # self.vk_friends = self.vk_session.friends.get()
#         # self.vk_groups = self.vk_session.groups.get()
#         # self.vk_wall = self.vk_session.wall.get(owner_id=self.vk_id)
#         # self.vk_messages = self.vk_session.messages.get(owner_id=self.vk_id)
#     def run(self):
#         for event in self.longpoll.listen():
#             if event.type == VkEventType.MESSAGE_NEW:
#                 msg = event.object.message
        
# if __name__ == '__main__':
#     VkBot().run()
        

# vk_session = vk_api.VkApi(token=main_token)
# longpoll = VkLongPoll(vk_session)

