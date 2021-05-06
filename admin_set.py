import logging

log = logging.getLogger('admin_set')

async def admin_set(event, cs: 'ChatScript') -> None:
    com = cs.message.split(' ')
    if len(com) >= 2:
        com = com[1].strip()
    else:
        if cs.reply:
            await event.reply("/msg Должен быть второй операнд число 'set 100'")
        else:
            await event.reply("/msg Должен быть второй операнд число 'set 100' и нужно отправлять реплаем")
    try:
        value = int(com)
        if cs.reply:
            if cs.s_nick:
                cs.s_karma = value
                await event.reply(f'% {cs.s_nick} теперь имеет значение кармы {value}')
            else:
                await event.reply(f'/msg Не могу присвоить, в базе нет этого человека')
        else:
            await event.reply(f'/msg Нужно отправлять реплаем')
    except ValueError:
        await event.reply(f'/msg Некорректное значение после set\n"{com}" - невозможно обработать')
    await event.reply('/del')
