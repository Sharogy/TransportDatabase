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
        self.cursor.execute("SHOW tables;")
        self.all_tables = [i[0] for i in self.cursor.fetchall()]
        self.constraints = {"customers": "customer_name",
                            "employees": "first_name",
                            "orders": "cargo_type",
                            "trucks": "description",
                            "offices": "office_location",
                            "users": "username"}

    def primary_keys(self, not_foreign: bool):
        assert self.table_name is not None
        self.cursor.execute("SHOW KEYS FROM {} WHERE Key_name = 'PRIMARY';".format(self.table_name))
        if not_foreign:
            return [i[4] for i in self.cursor.fetchall() if
                    'id' in i[4].lower() and i[4].split('_')[0] in self.table_name]
        else:
            return [i[4] for i in self.cursor.fetchall() if
                    'id' in i[4].lower()]

    def get_max_id(self) -> List:
        assert self.table_name is not None
        result = []
        prime_keys = self.primary_keys(True)
        for key in prime_keys:
            self.cursor.execute("SELECT MAX({}) FROM {};".format(key, self.table_name))
            result.append(int(self.cursor.fetchall()[0][0]))
        return result

    def multi_update(self, col: List, values: List, *args) -> str:
        base_cmd = """
            UPDATE {table_name}
            SET \n
        """.format(table_name=self.table_name)
        for c, v in zip(range(len(col)), range(len(values))):
            if c < len(col) - 1:
                base_cmd += "{col} = '{value}',\n".format(col=col[c],
                                                          value=values[v])
            else:
                base_cmd += "{col} = '{value}'\n".format(col=col[c],
                                                         value=values[v])
        base_cmd += "WHERE \n"
        prime_keys = self.primary_keys(False)
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
        prime_keys = self.primary_keys(False)
        for i1, i2 in zip(range(len(prime_keys)), range(len(args))):
            if i1 < len(prime_keys) - 1:
                base_cmd += "{} = '{}' and\n".format(prime_keys[i1], args[i2])
            else:
                base_cmd += "{} = '{}'".format(prime_keys[i1], args[i2])
        return base_cmd

    def prime_index(self) -> List:
        primary_keys = self.primary_keys(False)
        self.cursor.execute("SELECT * FROM {};".format(self.table_name))
        self.cursor.fetchall()
        indices = [primary_keys.index(i) for i in self.cursor.column_names if i in primary_keys]
        return indices

    def foreign_keys(self):
        self.cursor.execute("SELECT * FROM {};".format(self.table_name))
        self.cursor.fetchall()
        current_cols = self.cursor.column_names
        table_dict = {}
        for name in self.all_tables:
            self.cursor.execute("SELECT * FROM {};".format(name))
            self.cursor.fetchall()
            table_dict[name] = self.cursor.column_names
        all_foreigns = {}
        for col in current_cols:
            if "id" in col.lower():
                all_foreigns[col] = []
            for key, value in table_dict.items():
                if col in value and 'id' in col.lower():
                    all_foreigns[col].append(key)
        return all_foreigns

    def all_foreign_keys_selection(self) -> dict:
        keys = self.foreign_keys().keys()
        key_table = {}
        for k in keys:
            key_table[k] = k.split('_')[0] + 's'
        result_dict = {}
        for k, v in key_table.items():
            self.cursor.execute("SELECT {}, {} FROM {};".format(k, self.constraints[v], v))
            result_dict[k] = list(set(["{}, {}".format(i[0], i[1]) for i in self.cursor.fetchall()]))
        return result_dict
