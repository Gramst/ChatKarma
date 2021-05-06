import random, datetime, logging

from settings import NAME_SCRIPT, COM

log = logging.getLogger('bot_py_files.cl_message')

class MsgTEXT():

    def __init__(self, **kwargs):

        self.raw_text = kwargs.get("raw_text", "").strip()

    @property
    def tf_user_income_to_bot(self)-> bool:
        if self.raw_text.startswith('[Bot] '):
            if 'входит в чат' in self.raw_text.lower():
                return True
        return False
    
    @property
    def tf_new_user_income_to_bot(self)-> bool:
        if self.user_income_to_bot:
            if 'входит в чат' in self.raw_text.lower():
                return True
        return False


    @property
    def tf_user_message(self)-> bool:
        if self.raw_text.startswith(('[Bot]','[BOT] ', '* ')):
            return False
        return True

    @property
    def tf_third_user_message(self)-> bool:
        if self.raw_text.startswith('* '):
            return True
        return False

    @property
    def tf_change_nick(self)-> bool:
        if self.raw_text.startswith('[Bot] '):
            if ' сменил ник на ' in self.raw_text.lower() or 'переименован в ' in self.raw_text.lower():
                return True
        return False

    @property
    def tf_karma_change(self) -> int:
        if self.tf_user_message and len(self.raw_text.split(': '))>=2:
            if self.raw_text.split(': ')[1].strip().startswith(('+')):
                return 1
            if self.raw_text.split(': ')[1].strip().startswith(('-')):
                return -1
        return 0

    @property
    def tf_hide_user_message(self):
        if self.raw_text.startswith('Скрытое фото от '):
            return 'Скрытое фото от '
        if self.raw_text.startswith('Скрытый документ от '):
            return 'Скрытый документ от '
        if self.raw_text.startswith('Скрытое видео от '):
            return 'Скрытое видео от '
        return False

    @property
    def command(self):
    #поиск алиаса в сыром тексте и возврат соответствующей команды 
    #возвращает первое слово после ':'
    #DEPRECATED
        if self.tf_user_message:
            _txt = self.raw_text.split(':', maxsplit = 1)
            if len(_txt) >= 2:
                _txt = _txt[1].strip().lower()
            else:
                return None
            for i in COM.keys():
                finded = [j for j in COM[i] if j == _txt]
                if finded:
                    return i
        return None

    @property
    def tobe_ornot_tobe(self):
        if self.tf_user_message:
            if ' или ' in self.raw_text[len(self.nick) + 1 :] and len([i for i in self.raw_text[len(self.nick) + 1:].split(' ') if i]) <= 5:
                temp_var = list(self.raw_text[len(self.nick) + 1:].partition(' или '))
                if temp_var.count(' или ') == 1 and temp_var.index(' или ') == 1:
                        temp_var.pop(temp_var.index(' или '))
                        res = temp_var[random.randint(0, (len(temp_var) - 1))]
                        if not res.startswith(':'):
                            return res.strip()
        return False

    @property
    def text_message(self):
        splttext = self.raw_text.split(':', maxsplit=1)
        if len(splttext) == 2:
            return self.raw_text.split(':', maxsplit=1)[1].strip()
        else:
            return self.raw_text

    @property
    def new_nick(self):
        if ' сменил ник на ' in self.raw_text:
            return self.raw_text.partition(' сменил ник на ')[2].strip()
        if 'переименован в ' in self.raw_text:
            return self.raw_text.partition('переименован в ')[2].strip()
        return None

    def _stars_return_nick(self):
        if 'крепко обнимает #' not in self.raw_text and ' слегка шлёпнул #' not in self.raw_text:
            return self.raw_text[2:].split('  ')[0].strip()
        return None

    def _hide_return_nick(self):
        spacer = self.tf_hide_user_message
        if spacer:
            temp =  self.raw_text.partition(spacer)[2]
            if ": " in temp:
                temp = temp.split(' ')[1:-2]
                result = ''
                for i in temp:
                    result += (i + ' ')
                return result.strip()[:-1]
                
            else:
                temp = temp.split(' ')[1:]
                result = ''
                for i in temp:
                    result += (i + ' ')
                return result.strip()[:-1]
        return None

    def _rename_return_nick(self):
        spacer = None
        if ' сменил ник на ' in self.raw_text.lower():
            spacer = ' сменил ник на '
        elif 'переименован в ' in self.raw_text.lower():
            spacer = 'переименован в '
        if spacer:
            old_nick = self.raw_text.partition(' сменил ник на ')[0].split(' ')[2:]
            result_old = ''
            for i in old_nick:
                result_old += (i + ' ')
            return result_old.strip()
        return None

    def _standart_return_nick(self):
        return self.raw_text.split(':')[0].strip()

    def _rename_return_second_nick(self):
        if ' сменил ник на ' in self.raw_text:
            return self.raw_text.partition(' сменил ник на ')[2].strip()
        if 'переименован в ' in self.raw_text:
            return self.raw_text.partition('переименован в ')[2].strip()
        return None

    def _income_outcome_return_nick(self):
        msgsplit = self.raw_text.split()
        if len(msgsplit) >= 3:
            return msgsplit[2]
        return None

class ProcessedTelethMessage(MsgTEXT):

    def __init__(self, dict_tlth_message):
        self._dict_tlth_msg = dict_tlth_message
        self.name_script = NAME_SCRIPT
        self.out = self._dict_tlth_msg.get('out')
        self.msg_id = self._dict_tlth_msg.get('id')
        _ = self._dict_tlth_msg.get('reply_to')
        #log.info(f'DICT TLTH MSG : {self._dict_tlth_msg}')
        #log.info(f'GET FROM ^ : {_}')
        if _:
            self.reply_id = _.get('reply_to_msg_id')
            #log.info(f'FINDED : {self.reply_id}')
        else:
            self.reply_id = None
        text = None
        text = self.tf_sticker_message
        if not text:
            text = self._dict_tlth_msg.get('message', '')
        super().__init__(raw_text=text)

    @property
    def tf_sticker_message(self):
        try:
            nick = self._dict_tlth_msg['reply_markup']['rows'][0]['buttons'][0]['text']
            alt_text = self._dict_tlth_msg['media']['document']['attributes'][1]['alt']
            return  f'{nick}: {alt_text}'
        except Exception as ex:
            #log.error(ex)
            return None

    @property
    def nick(self):
        if not self.out:
            if self.tf_user_income_to_bot:
                return self._income_outcome_return_nick()
            if self.tf_change_nick:
                return self._rename_return_nick()
            if self.tf_third_user_message:
                return self._stars_return_nick()
            if self.tf_hide_user_message:
                return self._hide_return_nick()
            if self.tf_karma_change or self.tf_user_message:
                return self._standart_return_nick()
        return None
