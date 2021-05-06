import logging

from settings import NAME_CHAT

log = logging.getLogger('karma_change')

async def karma_change(event, client, cs: 'ChatScript') -> None:
    log.info('karma change start')
    if cs.m_hash == cs.s_hash:
        log.info(str(cs.m_nick) + " self like")
        await event.reply(f'{cs.m_nick} нежно погладил себя!)')
    elif cs.delta_karm > 0 and cs.like <= 0:
        cs.like = 1
        cs.s_karma += 1
        log.info(str(cs.m_nick) + " like " + str(cs.s_nick))
        await client.send_message(NAME_CHAT, f"% {cs.s_nick} +1 [{cs.s_karma}]")
    elif cs.delta_karm < 0 and cs.like >= 0:
        cs.like = -1
        cs.s_karma -= 1
        log.info(str(cs.m_nick) + " dislike " + str(cs.s_nick))
        await client.send_message(NAME_CHAT, f"% {cs.s_nick} -1 [{cs.s_karma}]")

