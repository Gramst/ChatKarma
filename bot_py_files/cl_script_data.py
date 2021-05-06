import json
import datetime
import logging
from bot_py_files.cl_message import ProcessedTelethMessage
from bot_py_files.cl_sup_varia import PrintSearchinDict, Cashe
from bot_py_files.cl_db import KarmaDB, MsgDB, LikedDB

class ChatScript():

    def __init__(self):
        self.userdb = KarmaDB()
        self.msgdb = MsgDB()
        self.likedb = LikedDB()

        self._m_nick = None
        self._s_nick = None
        self._m_karm = None
        self._s_karm = None
        self._m_hash = None
        self._s_hash = None
        self._like = None
        self._m_ach = None
        self._s_ach = None

        super().__init__()

    @property
    def message(self):
        return self._message.raw_text

    @message.setter
    def message(self, dict_tlth_message):
        print('MSG SETTER class ChatScript')
        self._message = ProcessedTelethMessage(dict_tlth_message)

        self.get_m_user()
        self.get_s_user()

        if self._m_nick and not self._m_hash:
            self.userdb.add_row(self._m_nick, self._message.msg_id)
            self.get_m_user()

        if self._m_nick and self._m_hash:
            self.msgdb.add_row(self._message.msg_id, self._m_nick, self._m_hash)

    def get_m_user(self):
        self._m_nick = self._message.nick
        self._m_hash, self._m_karm, self._m_ach = self.userdb.get_m_user(self._message.nick)
        self._like = self.likedb.check_like(self._message.reply_id, self._m_hash)

    def get_s_user(self):
        print('FIND S USER')
        self._s_hash = self.msgdb.get_hash(self._message.reply_id)
        self._s_nick, self._s_karm, self._s_ach = self.userdb.get_s_user(self._s_hash)

    @property
    def out(self):
        return self._message.out

    @property
    def reply(self):
        return self._message.reply_id


    @property
    def m_nick(self):
        return self._m_nick

    @m_nick.setter
    def m_nick(self, new_nick):
        self.userdb.update_nick(self._m_nick, new_nick)
        self._m_nick = new_nick

    @property
    def s_nick(self):
        return self._s_nick

    @property
    def m_hash(self):
        return self._m_hash

    @property
    def s_hash(self):
        return self._s_hash

    @property
    def m_karma(self):
        return self._m_karm

    @m_karma.setter
    def m_karma(self, value):
        self.userdb.set_new_karma_value(self._m_nick, value)
        self._m_karm = value

    @property
    def m_ach(self):
        return self._m_ach

    @m_ach.setter
    def m_ach(self, value):
        if value:
            self.userdb.set_ach(self.m_nick, value)
        # logging.INFO('m_ach setter pass change value')

    @property
    def s_karma(self):
        return self._s_karm

    @s_karma.setter
    def s_karma(self, value):
        self.userdb.set_new_karma_value(self._s_nick, value)
        self._s_karm = value

    @property
    def new_nick(self):
        return self._message.new_nick

    @property
    def delta_karm(self):
        return self._message.tf_karma_change

    @property
    def tobe(self):
        return self._message.tobe_ornot_tobe

    @property
    def command(self):
        return self._message.command

    @property
    def all_list(self):
        return self.userdb.get_all()

    @property
    def like(self):
        return self.likedb.check_like(self._message.reply_id, self._m_hash)

    @like.setter
    def like(self, val):
        if val > 0:
            if self._like < 0:
                self.likedb.del_like(self._message.reply_id, self._m_hash)
                self._like = 0
            elif self._like == 0:
                self.likedb.add_row(self._message.reply_id, self._m_nick, self._m_hash, 1)
                self._like =  1
        if val < 0:
            if self._like > 0:
                self.likedb.del_like(self._message.reply_id, self._m_hash)
                self._like = 0
            elif self._like == 0:
                self.likedb.add_row(self._message.reply_id, self._m_nick, self._m_hash, -1)
                self._like =  -1

    @property
    def status(self):
        if self.out:
            return 'out'

        if not self.out:
            if self._message.tf_user_income_to_bot:
                return 'us_income'
            if self._message.tf_change_nick:
                return 'ch_nick'
            if self._message.tf_karma_change:
                return 'ch_karma'
            if self._message.tobe_ornot_tobe:
                return 'tobeornot'
            if self._message.tf_user_message and self._m_nick:
                return 'normal_message'
        
        return None
