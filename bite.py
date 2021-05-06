import logging
import random

from settings import KARMA_TO_BITE_USE

log = logging.getLogger('bite')

BITE_TEXT = [
        '{0} делает кусь {1}. {1} испуганно морщится.',
        '{0} кусь за одну! {1} cмущаясь подставляет вторую.',
        '{0} делает критический кусь! {1} истекает кровью и бьётся в конвульсиях! {0} хищно улыбается',
        '{0} кусь {1}. {1} кричит "больно" и пытается убежать',
        '{0} по хозяйски кусь {1}. {1} cмиренно принимает вредность',
        '{0} ласково кусь {1}. {1} всеми силами пытается показать равнодушие',
        '{0} схватив {1} делает кусь! {1} молит о пощаде'
    ]

def get_act_text():
    return BITE_TEXT[random.randint(0, (len(BITE_TEXT)-1))]

async def make_bite(event, cs: 'ChatScript') -> None:
    if cs.m_karma >= KARMA_TO_BITE_USE and cs.s_nick:
        res = get_act_text().format(cs.m_nick, cs.s_nick)
        log.info(str(cs.m_nick) + " bite " + str(cs.s_nick))
        _ = await event.message.get_reply_message();
        await _.reply(res)
        #await event.reply(res)
    elif cs.m_karma < KARMA_TO_BITE_USE:
        log.info(str(cs.m_nick) + " fail bite " + str(cs.s_nick))
        await event.reply(f"/msg Нужно больше кармы милорд!\nБольше {KARMA_TO_BITE_USE}, а у Вас всего {cs.m_karma}")
    await event.reply("/del")
