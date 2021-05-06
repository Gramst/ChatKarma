import logging

log = logging.getLogger('admin_db')

async def admin_db(event, cs: 'ChatScript') -> None:
    com = cs.message.split(' ')
    if len(com) >= 3:
        com = com[2].strip()
    else:
        await event.reply("/msg Должен быть второй операнд:\nuser\nlike\nmsg\nall")
    if com == 'user':
        cs.userdb.clean()
        await event.reply("/msg userDB очищена")
    elif com == 'msg':
        cs.msgdb.clean()
        await event.reply("/msg msgDB очищена!\n+ к карме только после этого сообщения")
    elif com == 'like':
        cs.likedb.clean()
        await event.reply("/msg likeDB очищена полностью.")
    elif com == 'all':
        cs.userdb.clean()
        cs.msgdb.clean()
        await event.reply("/msg Базы userDB, msgDB очищены")
    await event.reply('/del')
