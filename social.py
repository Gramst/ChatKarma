import logging

log = logging.getLogger('social')

SOCIALS = {
    'smile' : ['sm', 'ул'],
    'laugh' : ['la', 'смех'],
    '?'     : ['?'],
}

S_TEXT = {
    'smile' : '% {0} мило улыбается {1}',
    'laugh' : '% {0} от души посмеялся с {1}',

}

S_TEXT_SELF = {
    'smile' : '% {0} мило улыбнулся',
    'laugh' : '% {0} от души посмеялся',
}

def get_text(text: str) -> str:
    _txt = text.split(':', maxsplit = 1)
    if len(_txt) == 2:
        _txt = _txt[1].strip()
        _txt = _txt.split(' ', maxsplit = 1)
        if len(_txt) == 2:
            return _txt[1].strip()
    return ''

def find_social_from_text(text: str) -> str:
    _txt = get_text(text)
    if _txt:
        for j in SOCIALS.keys():
            _ = [i for i in SOCIALS[j] if _txt == i]
            if _:
                return j, _txt.replace(_[0],'', 1)
        return '', _txt
    return '', ''

def form_help() -> str:
    res = 'Это социальная часть бота, позволяет отправлять заранее заготовленные сообщения, и свои'\
    '. Синтаксис: соц команда @1 тот кто отправляет @2 тот кому отправляют'
    for i in SOCIALS.keys():
        if i != '?':
            res += f"\nсоц {SOCIALS[i]} == {S_TEXT[i].format('@1', '@2')}"
    res += '\nДля отправки своего сообщения отправляете фразу начинающуюся на соц c метками @1 @2. @1 - ваш ник @2 - ник из реплая или будет откинуто и замененно пробелом'
    return res

async def social(event, cs: 'ChatScript') -> None:
    _ = await event.message.get_reply_message()
    s, custom = find_social_from_text(cs.message)
    if s and s == '?':
        h = form_help();
        await event.reply(f'/msg {h}')
    elif _ and cs.m_nick and cs.s_nick:
        if s:
            await _.reply(S_TEXT[s].format(cs.m_nick, cs.s_nick))
        elif custom:
            await _.reply('/say ' + custom.replace('@1', cs.m_nick).replace('@2', cs.s_nick))
    else:
        if s:
            await event.reply(S_TEXT_SELF[s].format(cs.m_nick))
        elif custom:
            await _.reply('/say ' + custom.replace('@1', cs.m_nick).replace('@2',''))
    await event.reply('/del')

            
