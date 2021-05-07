import logging

from settings import COM

log = logging.getLogger('social')

SOCIALS = {
    'smile' : ['sm', 'ул'],
    'hate'  : ['каквтомролике'],
}

S_TEXT = {
    'smile' : '% {0} мило улыбается {1}',
    'hate' :'% {0} выбегает за {1} и кричит ему вслед:\n Уб***ок, мать твою, а ну иди сюда г***о собачье, решил ко мне лезть? Ты, за***нец вонючий, мать твою, а?'\
    ' Ну иди сюда, попробуй меня тр***ть, я тебя сам тр**ну ублюдок, онанист чертов, будь ты проклят, иди ид**т, тр***ть тебя и всю семью,'\
    ' г**но собачье, ж**б вонючий, де**мо, с**а, п**ла, иди сюда, мерзавец, негодяй, гад, иди сюда ты - г**но, Ж*ПА!',

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

async def social(event, cs: 'ChatScript') -> None:
    _ = await event.message.get_reply_message()
    s, custom = find_social_from_text(cs.message)
    if s:
        await _.reply(S_TEXT[s].format(cs.m_nick, cs.s_nick))
    elif custom:
        await _.reply(f'{cs.m_nick} {custom} {cs.s_nick}')
    await event.reply('/del')

            
