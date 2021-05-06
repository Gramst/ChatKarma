import logging
from functools import reduce

from settings import KARMA_TO_KTOP, KARMA_TOP_Q

log = logging.getLogger('karma_top')

def karma_top_pic(val) -> str:
    top_smile = ['🤩','🤣','😂','😅','😆','😁','😄','😃','😀','🙂']
    val = int(val)
    if val <= 0:
        return '🤕'
    elif val <= len(top_smile):
        return top_smile[val-1]
    else:
        return '🤭'

async def form_top_karma(event, cs: 'ChatScript', check_settings = True) -> None:
    if not check_settings or cs.m_karma >= KARMA_TO_KTOP:
        c = ["{1:<4}:{0}".format(i[0], i[1]) for i in
             sorted(cs.all_list, key=lambda x: int(x[1]), reverse=True) if int(i[1]) != 0]
        res = f'\nTop {KARMA_TOP_Q} karmamaniac:'
        if c:
            num = [karma_top_pic(i) for i in range(1,KARMA_TOP_Q)]
            top_list = zip(c, num)
            top_list = map(lambda x: "\n" + str(x[1]) + ' ' + x[0], top_list)
            res += reduce(lambda a, x: a + x, top_list)
            res += "\n..."
        else:
            res += '\nНикого нет((('
        log.info(str(cs.m_nick) + " top use")
        await event.reply(res)
    else:
        log.info(str(cs.m_nick) + " can't top use")
        await event.reply(f"/msg Нужно больше кармы милорд!\nБольше {KARMA_TO_KTOP}, а у Вас всего {cs.m_karma}")

    await event.reply("/del")
