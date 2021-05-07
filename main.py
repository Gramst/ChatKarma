from telethon import TelegramClient, events
import logging

from bot_py_files.f_text import TEXT_HELP, TEXT_ADMIN_HELP
from bot_py_files.cl_script_data import ChatScript

from karma_top import form_top_karma
from admin_db import admin_db
from bite import make_bite
from admin_set import admin_set
from karma_change import karma_change
from social import social

from settings import *
from SECRET import *

client = TelegramClient(tel_number, api_id, api_hash)

def get_command_from_user_message(text: str) -> str:
    if text:
        _txt = text.split(':', maxsplit = 1)
        if len(_txt) >= 2:
            _txt = _txt[1].strip().lower()
        else:
            return ''
        for i in COM.keys():
            finded = [j for j in COM[i] if j == _txt]
            if finded:
                return i
    return ''

def get_startswith_command(text: str) -> str:
    if text:
        _txt = text.split(':', maxsplit = 1)
        if len(_txt) >= 2:
            _txt = _txt[1].strip().lower()
        else:
            return ''
        for i in COM.keys():
            finded = [j for j in COM[i] if _txt.startswith(j)]
            if finded:
                return i
    return ''

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('main')
    cs = ChatScript()

    @client.on(events.NewMessage(chats=(NAME_CHAT)))
    async def normal_handler(event):

        cs.message = event.message.to_dict()
        print(event.message.to_dict())
        logging.info("MSG: " + str(cs._message.raw_text))
        logging.info(str(cs.m_nick) + ' (' + str(cs.status) + ') to ' + str(cs.s_nick))

        if cs.out:
            msg = cs.message.lower()
            if msg == 'test' or msg == 'тест':
                await form_top_karma(event, cs, False)
            elif msg in COM['help']:
                await event.reply('/msg ' + TEXT_ADMIN_HELP)
                await event.reply('/del')
            elif [i for i in COM['a_db'] if msg.startswith(i)]:
                await admin_db(event, cs) 
            elif [i for i in COM['a_ks'] if msg.startswith(i)]:
                await admin_set(event, cs)
        else:
            #COMMANDS
            user_command = get_command_from_user_message(cs.message) 
            user_stw_comm = get_startswith_command(cs.message)
            logging.info(f'USER COM {user_command}')
            if user_command == 'help':
                logging.info(str(cs.m_nick) + " help use")
                await event.reply('/msg ' + TEXT_HELP)
                await event.reply("/del")
            elif user_command == 'karm':
                if cs.reply:
                    await event.reply("/msg Карма: {0}\n[{1}] {2:<4}🎭".format(cs.s_nick, cs.s_hash, cs.s_karma))
                    await event.reply("/del")
                else:
                    await event.reply("/msg Карма: {0}\n[{1}] {2:<4}🎭".format(cs.m_nick, cs.m_hash, cs.m_karma))
                    await event.reply("/del")
            elif user_command == 'ktop':
                await form_top_karma(event, cs)
            elif user_command == 'bite':
                await make_bite(event, cs)
            elif user_stw_comm == 'soci': #TODO условия
                await social(event, cs)
            #STATUS    
            log.info(f'{cs.status}, {cs.m_karma}, {cs.s_nick}')
            if cs.status == 'ch_nick':
                logging.info(str(cs.m_nick) + " nick change " + str(cs.new_nick))
                cs.m_nick = cs.new_nick
            elif cs.status == 'ch_karma' and cs.m_karma >= MIN_KARMA_TO_USE and cs.s_nick: #TODO изменить условие
                await karma_change(event, client, cs)    
            elif cs.status == 'tobeornot' and not cs.reply:
                logging.info(str(cs.m_nick) + " to be or not ")
                await event.reply(f"Твой выбор:\n{cs.tobe}")
            elif cs.status == 'us_income':
                if 'ходит в чат. он новенький!' in cs.message.lower():
                    msgsplit = cs.message.split()
                    playmsg = "Привет! " + str(msgsplit[2]) + "!\nУ нас есть правила /rules, если согласен - добро "\
                                                            "пожаловать!\nМеняй ник /nick и вливайся.\n"\
                                                           f"Если интересно больше узнать про карму просто напиши {COM['help']}"
                    logging.info(str(cs.m_nick) + " new user")
                    await event.reply(playmsg)
                else:
                    logging.info(str(cs.m_nick) + " old income")
                    await event.reply('Привет! Рад тебя видеть снова!')

    client.start()
    client.run_until_disconnected()
