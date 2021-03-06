import sqlite3

class BaseDB():
    
    def __init__(self, **kwargs):

        self.base_name = kwargs.get('base_name', False)
        if not self.base_name:
            assert False, f"Need db name {self.__name__}"
        self.path = kwargs.get('path', '')
        self.conn = sqlite3.connect(self.path+self.base_name)
        self.cursor = self.conn.cursor()

        self.table_column = kwargs.get('table_column', False)
        if not self.table_column:
            assert False, f"Fail column {self.__name__}"

        self.table_name = kwargs.get('table_name', False)
        if not self.table_name:
            assert False, f"Fail table_name {self.__name__}"

        print(f"CREATE TABLE {self.table_name} ({self.table_column})")

        try:
            self.cursor.execute(
                f""" 
                CREATE TABLE {self.table_name}
                ({self.table_column})
                """
            )
        except:
            pass
        
        self.cursor.execute(f"""select * from {self.table_name}""")
        exist_colums = [descr[0] for descr in self.cursor.description]
        
        column_to_remove = []
        self.name_columns = self.table_column.split(', ')
        
        if self.name_columns != exist_colums:
            for i in exist_colums:
                try:
                    self.name_columns.remove(i)
                except ValueError:
                    # column_to_remove.append(i)
                    pass
            
            for i in self.name_columns:
                self.add_column(i)
            
            self.remove_column()

            self.cursor.execute(f"""select * from {self.table_name}""")
            self.name_columns = [descr[0] for descr in self.cursor.description]

        self.field_numbers = len(self.name_columns)
        self.sql_append = "INSERT INTO {0} VALUES ({1}{2})".format(self.table_name, "?, "*(self.field_numbers-1), "?")
        print(self.sql_append)

    def add_row(self, *args):

        if len(args) < self.field_numbers:
            res = list(args)
            add = [0 for i in range(self.field_numbers - len(args))]
            res.extend(add)
        elif len(args) == self.field_numbers:
            res = args
        else:
            pass

        self.cursor.executemany(self.sql_append, [res])
        self.conn.commit()

    def add_column(self, name):
        self.cursor.execute(f"""ALTER TABLE {self.table_name} ADD COLUMN {name}""")

    def remove_column(self):
        name_backup = self.table_name + "_backup"
        self.cursor.execute(f"""CREATE TABLE {name_backup} AS SELECT {self.table_column} FROM {self.table_name}""")
        self.cursor.execute(f"""DROP TABLE {self.table_name}""")
        self.cursor.execute(f"""ALTER TABLE {name_backup} RENAME TO {self.table_name}""")

    def clean(self):
        sql = f"DELETE FROM {self.table_name}"
        self.cursor.execute(sql)
        self.conn.commit()

######################################################
#
#
#
######################################################

class MsgDB(BaseDB):

    def __init__(self, **kwargs):
        kwargs['table_column'] = "msg_id, nick, hash"
        kwargs['base_name'] = 'script.db'
        kwargs['table_name'] = 'msg'
        super().__init__(**kwargs)

    def get_hash(self, msg_id):
        print(f'MSG DB SEARCH HASH FROM MSG ID {msg_id}')
        sql_search = f"SELECT hash FROM {self.table_name} WHERE msg_id=?"
        self.cursor.execute(sql_search, [(msg_id)])
        res =  self.cursor.fetchone()
        print(f'RESULT {res} <- return [0]')
        if res:
            return res[0]
        else:
            return None

######################################################
#
#
#
######################################################


class LikedDB(BaseDB):
    def __init__(self, **kwargs):
        kwargs['table_column'] = "msg_id, nick, hash, val"
        kwargs['base_name'] = 'script.db'
        kwargs['table_name'] = 'like'
        super().__init__(**kwargs)

    def check_like(self, msg_id, hash_user):
        if msg_id == None:
            msg_id = 0
        if hash_user == None:
            hash_user = 0
        sql_search = f"SELECT val FROM {self.table_name} WHERE msg_id={msg_id} AND hash={hash_user}"
        self.cursor.execute(sql_search)
        res = self.cursor.fetchone()
        if res:
            return int(res[0])
        else:
            return 0

    def del_like(self, msg_id, hash_user):
        sql = f"DELETE FROM {self.table_name} WHERE msg_id={msg_id} AND hash={hash_user}"
        self.cursor.execute(sql)
        self.conn.commit()


######################################################
#
# Main DB user karma etc
#
######################################################



class KarmaDB(BaseDB):

    def __init__(self, **kwargs):
        kwargs['table_column'] = "nick, hash, karma, adm, ach"
        kwargs['base_name'] = 'script.db'
        kwargs['table_name'] = 'users'
        super().__init__(**kwargs)

    def get_m_user(self, nick):
        sql_search = f"SELECT hash, karma, ach FROM {self.table_name} WHERE nick=?"
        self.cursor.execute(sql_search, [(nick)])
        res =  self.cursor.fetchone()
        if res:
            return int(res[0]), int(res[1]), res[2]
        else:
            return None, None, None

    def get_s_user(self, hash_user):
        sql_search = f"SELECT nick, karma, ach FROM {self.table_name} WHERE hash=?"
        self.cursor.execute(sql_search, [(hash_user)])
        res =  self.cursor.fetchone()
        if res:
            return res[0], int(res[1]), res[2]
        else:
            return None, None, None


    def set_ach(self, nick, value):
        value = str(value)
        sql = f"""
        UPDATE {self.table_name} 
        SET ach = '{value}' 
        WHERE nick = '{nick}'
        """       
        self.cursor.execute(sql)
        self.conn.commit()

    def set_new_karma_value(self, nick, value):
        value = str(value)
        sql = f"""
        UPDATE {self.table_name} 
        SET karma = '{value}' 
        WHERE nick = '{nick}'
        """       
        self.cursor.execute(sql)
        self.conn.commit()

    def update_nick(self, old_nick, new_nick):
        sql = f"""
        UPDATE {self.table_name} 
        SET nick = '{new_nick}' 
        WHERE nick = '{old_nick}'
        """       
        self.cursor.execute(sql)
        self.conn.commit()

    def get_all(self):
        sql = f"SELECT nick, karma, hash FROM {self.table_name}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def change_admin_status(self, hash_user):
        hash_user = int(hash_user)
        sql = f"SELECT adm, nick FROM {self.table_name} WHERE hash=?"
        self.cursor.execute(sql, [(hash_user)])
        res = self.cursor.fetchone()
        print(isinstance(res[0], int))
        if res[0] == 0:
            sql = f"""
            UPDATE {self.table_name} 
            SET adm = '1' 
            WHERE hash = {hash_user}
            """
        else:
            sql = f"""
            UPDATE {self.table_name} 
            SET adm = '0' 
            WHERE hash = {hash_user}
            """
        self.cursor.execute(sql)
        self.conn.commit()

    def clean(self):
        sql = f"DELETE FROM {self.table_name} WHERE karma=0"
        self.cursor.execute(sql)
        self.conn.commit()

if __name__ == "__main__":
    a= KarmaDB()

    print(a.get_m_user('?????????????????? ????????????'))
    print(a.get_s_user(649966))

    a.set_ach('?????????????????? ????????????', '????')

    print(a.get_m_user('?????????????????? ????????????'))

