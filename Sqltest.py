import mysql.connector

class SQL_DB:

    host_id = ""
    user = ""
    password = ""

    db = None

    def __init__(self, host_id, user, password):
        self.host_id = host_id
        self.user = user
        self.password = password

        self.connect_to_sql_server()
        # self.show_all_dbs()

    def connect_to_sql_server(self):
        self.all_dbs = mysql.connector.connect(
            host=self.host_id,
            user=self.user,
            password=self.password
        )

        self.create_all_dbs_cursor()

    def create_all_dbs_cursor(self):
        self.cursor_all_dbs = self.all_dbs.cursor()

    def show_all_dbs(self):
        self.cursor_all_dbs.execute("SHOW DATABASES")

        for x in self.cursor_all_dbs:
            print(x)

    def create_db(self, name):
        self.cursor_all_dbs.execute(f"CREATE DATABASE {name}")


    def connect_to_db(self, db_name):
        self.db = mysql.connector.connect(
            host=self.host_id,
            user=self.user,
            password=self.password,
            database = db_name
        )

        self.create_db_cursor()
    
    def create_db_cursor(self):
        self.cursor_db = self.db.cursor(buffered=True)

    def show_all_tabels(self):
        self.cursor_db.execute("SHOW TABLES")

        for x in self.cursor_db:
            print(x)


    def foreign_key_checks(self):
        sql = "SET FOREIGN_KEY_CHECKS=0;"

        self.cursor_db.execute(sql)


    def insert(self, table_name, value_one, value_two=None, value_three=None, value_four=None, value_five=None, value_six=None, value_seven=None, value_eight=None, value_nine=None, value_ten=None, value_eleven=None, value_twelve=None, value_thirteen=None, value_fourteen=None):
        fields_and_values = {
            "nachtposition":["(Position, Discord_ID, Rollen_ID, Spiel_ID)", "(%s, %s, %s, %s)"],
            "spiele": ["(Server_ID, Erzaehler_ID)", "(%s, %s)"],
            "spieler": ["(Spiel_ID, Discord_ID, Discord_Name, Previous_Voice_Channel)", "(%s, %s, %s, %s)"],
            "temp_tabelle": ["(Spiel_ID, Beschreibung, Wert)", "(%s, %s, %s)"],
            "temp_rollen_im_spiel": ["(Spiel_ID, Rollen_ID)", "(%s, %s)"]
        }

        current_fields_and_values = fields_and_values[table_name]
        self.foreign_key_checks()

        sql = f"INSERT INTO {table_name} {current_fields_and_values[0]} VALUES {current_fields_and_values[1]}"
        val = [value_one, value_two, value_three, value_four, value_five, value_six, value_seven, value_eight, value_nine, value_ten, value_eleven, value_twelve, value_thirteen, value_fourteen]
        for i in val:
            if i == None:
                val = val[:val.index(i)]
                break
            else:
                if type(i) == bool:
                    index = val.index(i)
                    val[index] = int(i)
                    val[index] = str(val[index])
                else:
                    val[val.index(i)] = str(i)
        val = tuple(val)
        # print(val)

        self.cursor_db.execute(sql, val)

        self.db.commit()

        # print(self.cursor_db.rowcount, "record inserted.")
        return f"{self.cursor_db.rowcount} record inserted."

    def select_all_from_table(self, column, table_name):
        self.cursor_db.execute(f"SELECT {column} FROM {table_name}")

        myresult = self.cursor_db.fetchall()

        # for x in myresult:
        #     print(x)
        
        return myresult
    
    def select_where_from_table(self, column, table_name, statement, value, statement1 = None, value1 = None):
        sql = f"SELECT {column} FROM {table_name} WHERE {statement} = %s"
        val = (value, )

        if statement1 and value1:
            sql += f" AND {statement1} = %s"
            val = (value, value1)

        self.cursor_db.execute(sql, val)

        myresult = self.cursor_db.fetchall()

        # for x in myresult:
        #     print(x)
        
        return myresult
    
    def delete_where_from_table(self, table_name, statement, value, statement1 = None, value1 = None):
        sql = f"DELETE FROM {table_name} WHERE {statement} = %s"
        val = (value, )

        if statement1 and value1:
            sql += f" AND {statement1} = %s"
            val = (value, value1)
       

        self.cursor_db.execute(sql, val)

        self.db.commit()

        # print(self.cursor_db.rowcount, "record(s) deleted")
        return f"{self.cursor_db.rowcount} record(s) deleted."
    
    def update_where_from_table(self, table_name, statement_set, value_new, statement_where, value_old):
        sql = f"UPDATE {table_name} SET {statement_set} = %s WHERE {statement_where} = %s"
        val = (value_new, value_old)

        self.cursor_db.execute(sql, val)

        self.db.commit()

        # print(self.cursor_db.rowcount, "record(s) affected")
        return f"{self.cursor_db.rowcount} record(s) affected."

    def count_entries_from_table(self, entry, table_name, statement, value, statement1 = None, value1 = None):
        sql = f"SELECT COUNT({entry}) from {table_name} WHERE {statement} = %s"
        val = (value, )

        if statement1 and value1:
            sql += f" AND {statement1} = %s"
            val = (value, value1)

        print(sql)
        self.cursor_db.execute(sql, val)

        self.db.commit()

        # print(self.cursor_db.rowcount, "record(s) affected")
        return self.cursor_db.fetchone()[0]

    def clear_all_tables(self, guild_id):
        spiel_id = self.select_where_from_table("Spiel_ID","spiele", "Server_ID", guild_id)[0][0]
        self.delete_where_from_table('spieler', 'Spiel_ID', spiel_id)
        self.delete_where_from_table('nachtposition', 'Spiel_ID', spiel_id)
        self.delete_where_from_table('spiele', 'Spiel_ID', spiel_id)
        self.delete_where_from_table('temp_tabelle', 'Spiel_ID', spiel_id)
        self.delete_where_from_table('temp_rollen_im_spiel','Spiel_ID', spiel_id)


# DELETE FROM temp_rollen_im_spiel LEFT JOIN rollen ON rollen.Rollen_id = temp_rollen_im_spiel.Rollen_id WHERE temp_rollen_im_spiel.Spiel_id = <statement> AND rollen.Is_Werwolf = 1
