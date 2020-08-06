import mysql.connector
from typing import List


class Database:
    def __init__(self, table_name: str = None):
        self.mydb = mysql.connector.connect(
            host="remotemysql.com",
            user="uqh0AMNV9Q",
            passwd="FNhLNozskh",
            database="uqh0AMNV9Q",
            auth_plugin='mysql_native_password',
            port=3306
        )
        self.table_name = table_name
        self.cursor = self.mydb.cursor()

    def primary_keys(self):
        assert self.table_name is not None
        self.cursor.execute("SHOW KEYS FROM {} WHERE Key_name = 'PRIMARY';".format(self.table_name))
        return [i[4] for i in self.cursor.fetchall() if 'id' in i[4].lower()]

    def get_max_id(self) -> List:
        assert self.table_name is not None
        result = []
        prime_keys = self.primary_keys()
        for key in prime_keys:
            self.cursor.execute("SELECT MAX({}) FROM {};".format(key, self.table_name))
            result.append(int(self.cursor.fetchall()[0][0]))
        return result

    # def id_change(self, lst=None, change: int = 1) -> List:
    #     max_ids = self.get_max_id()
    #     if lst is None:
    #         result = list(map(lambda i: i + change, max_ids))
    #     else:
    #         result = list(map(lambda i: i + change, lst))
    #     return result

    def multi_update(self, col, value, *args) -> str:
        base_cmd = """
            UPDATE {table_name}
            SET 
                {col} = '{value}'
            WHERE 
        """.format(table_name=self.table_name,
                   col=col,
                   value=value)
        prime_keys = self.primary_keys()
        for i1, i2 in zip(range(len(prime_keys)), range(len(args))):
            if i1 < len(prime_keys) - 1:
                base_cmd += "{} = '{}' and\n".format(prime_keys[i1], args[i2])
            else:
                base_cmd += "{} = '{}'".format(prime_keys[i1], args[i2])
        return base_cmd

    def multi_delete(self, *args):
        base_cmd = """
        DELETE FROM {table_name} 
        WHERE 
        """.format(table_name=self.table_name)
        prime_keys = self.primary_keys()
        for i1, i2 in zip(range(len(prime_keys)), range(len(args))):
            if i1 < len(prime_keys) - 1:
                base_cmd += "{} = '{}' and\n".format(prime_keys[i1], args[i2])
            else:
                base_cmd += "{} = '{}'".format(prime_keys[i1], args[i2])
        return base_cmd

    def prime_index(self):
        primary_keys = self.primary_keys()
        self.cursor.execute("SELECT * FROM {};".format(self.table_name))
        self.cursor.fetchall()
        indices = [primary_keys.index(i) for i in self.cursor.column_names if i in primary_keys]
        return indices
