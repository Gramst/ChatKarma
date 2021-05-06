from telethon import TelegramClient, events
from functools import reduce
import logging

from bot_py_files.f_text import get_act_text, karma_top_pic, TEXT_HELP, command_ach, surprize, cookie_text, TEXT_ADMIN_HELP
from bot_py_files.cl_script_data import ChatScript

from settings import *
from SECRET import *

client = TelegramClient(tel_number, api_id, api_hash)
if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)
    cs = ChatScript()

    @client.on(events.NewMessage(chats=(NAME_CHAT)))
    async def normal_handler(event):

        cs.message = event.message.to_dict()
        print(event.message.to_dict())
        logging.info("MSG: " + str(cs._message.raw_text))
        logging.info(str(cs.m_nick) + ' (' + str(cs.status) + ') to ' + str(cs.s_nick))

        if cs.out:
            msg = cs.message.lower()

            if msg in COM['help']:
                await event.reply(TEXT_ADMIN_HELP)

            if msg.startswith('karma clean') or msg.startswith('очистить базу'):
                com = cs.message.split(' ')
                if len(com) >= 3:
                    com = com[2].strip()
                else:
                    await event.reply("Должен быть второй операнд:\nuser\nlike\nmsg\nall")
                if com == 'user':
                    cs.userdb.clean()
                    await event.reply("userDB очищена")
                elif com == 'msg':
                    cs.msgdb.clean()
                    await event.reply("msgDB очищена!\n+ к карме только после этого сообщения")
                elif com == 'like':
                    cs.likedb.clean()
                    await event.reply("likeDB очищена полностью.")
                elif com == 'all':
                    cs.userdb.clean()
                    cs.msgdb.clean()
                    await event.reply("Базы userDB, msgDB очищены")

        if not cs.out:

            if cs.command == 'help':
                logging.info(str(cs.m_nick) + " help use")
                await event.reply('/msg ' + TEXT_HELP)
                await event.reply("/del")

            if cs.command == 'karm':
                if cs.reply:
                    await event.reply("/msg Карма: {0}\n[{1}] {2:<4}🎭".format(cs.s_nick, cs.s_hash, cs.s_karma))
                    await event.reply("/del")
                else:
                    await event.reply("/msg Карма: {0}\n[{1}] {2:<4}🎭".format(cs.m_nick, cs.m_hash, cs.m_karma))
                    await event.reply("/del")

            if cs.command == 'ktop':
                if cs.m_karma >= KARMA_TO_KTOP:
                    c = ["{1:<4}:{0}".format(i[0], i[1]) for i in
                         sorted(cs.all_list, key=lambda x: int(x[1]), reverse=True) if int(i[1]) != 0]
                    res = f'\nTop {KARMA_TOP_Q} karmamaniac:'
                    num = [karma_top_pic(i) for i in range(1,KARMA_TOP_Q)]
                    top_list = zip(c, num)
                    top_list = map(lambda x: "\n" + str(x[1]) + ' ' + x[0], top_list)
                    res += reduce(lambda a, x: a + x, top_list)
                    res += "\n..."
                    logging.info(str(cs.m_nick) + " top use")
                    await event.reply(res)
                else:
                    logging.info(str(cs.m_nick) + " can't top use")
                    await event.reply(f"/msg Нужно больше кармы милорд!\nБольше {KARMA_TO_KTOP}, а у Вас всего {cs.m_karma}")
                    await event.reply("/del")

            if cs.status == 'ch_nick':
                logging.info(str(cs.m_nick) + " nick change " + str(cs.new_nick))
                cs.m_nick = cs.new_nick

            if cs.status == 'ch_karma' and cs.m_karma >= 0 and cs.s_nick:
                if cs.m_hash == cs.s_hash:
                    logging.info(str(cs.m_nick) + " self like")
                    await event.reply(f'{cs.m_nick} нежно погладил себя!)')
                elif cs.delta_karm > 0 and cs.like <= 0:
                    cs.like = 1
                    cs.s_karma +=1
                    logging.info(str(cs.m_nick) + " like " + str(cs.s_nick))

                    await client.send_message(NAME_CHAT, f"% {cs.s_nick} +1 [{cs.s_karma}]")
                elif cs.delta_karm < 0 and cs.like >= 0:
                    cs.like = -1
                    cs.s_karma -=1
                    logging.info(str(cs.m_nick) + " dislike " + str(cs.s_nick))
                    await client.send_message(NAME_CHAT, f"% {cs.s_nick} -1 [{cs.s_karma}]")

            if cs.command == 'bite':
                if cs.m_karma >= KARMA_TO_BITE_USE and cs.s_nick:
                    res = get_act_text("bite").format(cs.m_nick, cs.s_nick)
                    logging.info(str(cs.m_nick) + " bite " + str(cs.s_nick))
                    await event.reply(res)
                elif cs.m_karma < KARMA_TO_BITE_USE:
                    logging.info(str(cs.m_nick) + " fail bite " + str(cs.s_nick))
                    await event.reply(f"/msg Нужно больше кармы милорд!\nБольше {KARMA_TO_BITE_USE}, а у Вас всего {cs.m_karma}")
                    await event.reply("/del")

            if cs.status == 'tobeornot' and not cs.reply:
                logging.info(str(cs.m_nick) + " to be or not ")
                await event.reply(f"Твой выбор:\n{cs.tobe}")

            if cs.status == 'us_income':
                if 'ходит в чат. он новенький!' in cs.message.lower():
                    msgsplit = cs.message.split()
                    playmsg = "Привет! " + str(msgsplit[2]) + "!\nУ нас есть правила /rules, если согласен - добро " +\
                                                            "пожаловать!\nМеняй ник /nick и вливайся.\n" +\
                                                           f"Если интересно больше узнать про карму просто напиши {COM['help']}"
                    logging.info(str(cs.m_nick) + " new user")
                    await event.reply(playmsg)
                else:
                    logging.info(str(cs.m_nick) + " old income")
                    await event.reply('Привет! Рад тебя видеть снова!')


    client.start()
    client.run_until_disconnected()
