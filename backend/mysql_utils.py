import mysql.connector as mysql
import time


class MySqlUtils:

    def __init__(self, host: str, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.__establish_connection__()
        self.__create_cursor__()


    def __establish_connection__(self):
        try:
            self.database_connection = mysql.connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                database=self.database
            )
            return self.database_connection

        except ConnectionError:
            print(f"Could not connect to the server on '{self.host}:{self.port}'!")
            exit(-1)

    def __create_cursor__(self):
        self.database_cursor = self.database_connection.cursor(buffered=True)
        return self.database_cursor

    def insert_user(self, table_name, firstname, lastname, dob, email, password, two_fa_code, permissions, profilepic, fav_dataset):

        self.exec(f"INSERT INTO {table_name} (vorname, nachname, geburtsdatum, email, passwort, 2_fa_code, rechte, profilbild, lieblingsdaten) VALUES ('{firstname}', '{lastname}', '{dob}', '{email}', '{password}', '{two_fa_code}', '{permissions}', '{profilepic}', '{fav_dataset}');")

    def find_by_key_value(self, table, key, value):

        return self.exec(f"SELECT * FROM {table} WHERE {key}='{value}';")

    def get_value_by_key_value(self, table, key, key2, value):

        return self.exec(f"SELECT {key2} FROM {table} WHERE {key}='{value}';")

    def exec(self, command: str):
        """
        Execute your own command. For everything that has not been implemented (yet).
        :param command: The command you want to execute.
        :return: The result of your command.
        """

        if not self.database_connection.is_connected():
            self.database_connection.reconnect()
            self.__create_cursor__()

        self.database_cursor.execute(command)
        self.database_connection.commit()
        try:
            # If there are any results return them!
            return self.database_cursor.fetchall()
        except Exception as e:
            # If there are no results return -1!
            return -1

    def get_tables(self):
        # Iterate over the given result and append it to the list (tables)
        tables = [[table[0] for table in self.exec("SHOW TABLES;")]]

        # Iterate over the given result and append it to the list (tables)
        tables.append([self.exec(f"SELECT TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tb_name}';")[0][0] for tb_name in tables[0]])

        return tables

    def get_dataset(self, table_name: str):
        """
        Retrieve the dataset from the database
        :param table_name: The table you want to fetch the data from
        :return: List containing everything
        """
        # Get the table header from a database table
        table_header = [column[0] for column in self.exec(f"DESCRIBE {table_name};")]

        table = self.exec(f"SELECT * FROM {table_name};")

        return [table_header] + table

    def get_row(self, table_name, row_name):

        return self.exec(f"""
                            SELECT 
                            {row_name}
                            FROM 
                            {table_name};
                            """)

    def update_value(self, table, email_id, key, value):

        return self.exec(f"UPDATE {table} SET {key}='{value}' WHERE email='{email_id}';")

    def update_row(self, table_name, keys: list, values: list):
        print(keys)
        build_str = ""
        for i in range(0, len(keys)):
            if i < len(keys) - 1:
                build_str += f"{list(keys)[i]} = '{list(values)[i]}', "
            else:
                build_str += f"{list(keys)[i]} = '{list(values)[i]}'"

        print(f"UPDATE {table_name} SET {build_str} WHERE keys='{list(values)[0]}';")
        return self.exec(f"UPDATE {table_name} SET {build_str} WHERE dataset_uid='{list(values)[0]}';")

    def delete_row(self, table_name, entry_uid):

        return self.exec(f"DELETE FROM {table_name} WHERE dataset_uid='{entry_uid}';")

    def insert_support_ticket(self, table_name, ticket_name, short_desc, long_desc, creator, status):

        return self.exec(f"INSERT INTO {table_name} (ticket_name, short_desc, long_desc, creator, status) VALUES ('{ticket_name}', '{short_desc}', '{long_desc}', '{creator}', '{status}');")

    def get_freunde(self, table_name, email_id):

        result = self.exec(f"SELECT email_id FROM {table_name} WHERE friend_email_id='{email_id}' AND status='friends';")
        result += [elem for elem in self.exec(f"SELECT friend_email_id FROM {table_name} WHERE email_id='{email_id}' AND status='friends';")]

        if len(result) == 0:
            result = [["Du hast noch keine Freunde. Füge sie jetzt hinzu!"]]

        return result

    def remove_friend(self, table_name, email_id, friend_email_id):

        return self.exec(f"DELETE FROM {table_name} WHERE email_id = '{email_id}' AND friend_email_id = '{friend_email_id}' OR email_id = '{friend_email_id}' AND friend_email_id = '{email_id}';")

    def add_friend(self, table_name, email_id, friend_email_id, timestamp):
        if friend_email_id not in self.get_freunde(table_name, email_id):

            return self.exec(f"INSERT INTO {table_name} (email_id, friend_email_id, status, action_timestamp) VALUES ('{email_id}', '{friend_email_id}', 'request-sent', '{timestamp}');")

        return -1

    def accept_friend(self, table_name, email_id, friend_email_id):

        return self.exec(f"UPDATE {table_name} SET status = 'friends' WHERE friend_email_id='{email_id}' AND email_id='{friend_email_id}';")

    def decline_friend(self, table_name, email_id, friend_email_id):

        return self.exec(f"DELETE FROM {table_name} WHERE status = 'request-sent' AND friend_email_id='{email_id}' AND email_id='{friend_email_id}';")

    def get_freundschaftsanfragen(self, email_id):
        time.sleep(.1)

        return self.exec(f"""SELECT email_id FROM freunde WHERE friend_email_id = '{email_id}' AND status='request-sent';""")

    def get_user_profilbild(self, user):

        return self.exec(f"""SELECT profilbild FROM user_data WHERE email = '{user}';""")[0]

    def get_freundesichtbarkeit(self, user):
        """
        :param user: The user you want to get the friend list visibility from
        :return: public / private
        """

        return self.exec(f"""SELECT sichtbarkeit FROM freundesichtbarkeit WHERE email_id = '{user}';""")[0]

    # ToDo: Namen ändern (diese Funktion ist nur für die initiale Erstellung eines Eintrags!)
    def set_freundesichtbarkeit(self, user, sichtbarkeit):

        return self.exec(f"""INSERT INTO freundesichtbarkeit (email_id, sichtbarkeit) VALUES ('{user}', '{sichtbarkeit}');""")

    def update_freundesichtbarkeit(self, user, sichtbarkeit):

        return self.exec(
            f"""UPDATE freundesichtbarkeit SET sichtbarkeit = '{sichtbarkeit}' WHERE email_id = '{user}';""")

    def set_profilsichtbarkeit(self, user, sichtbarkeit):

        return self.exec(f"""INSERT INTO profilsichtbarkeit (email_id, sichtbarkeit) VALUES ('{user}', '{sichtbarkeit}');""")


    def update_profilsichtbarkeit(self, user, sichtbarkeit):

        return self.exec(f"""UPDATE
                            profilsichtbarkeit
                            SET sichtbarkeit = '{sichtbarkeit}'
                            WHERE email_id = '{user}';
                            """)

    def save_message(self, sender, receiver, message, read, timestamp):

        self.exec(f"INSERT INTO messages (sender, receiver, message, read_status, unix_timestamp) VALUES ('{sender}', '{receiver}', '{message}', '{read}', '{timestamp}');")

    def save_group_message(self, sender, group, message):

        self.exec(f"INSERT INTO group_chat (sender, group_chat, message) VALUES ('{sender}', '{group}', '{message}');")

    def load_chat_history(self, user, chat_partner):
        print(f"UPDATE messages SET read_status = 'read' WHERE sender = '{chat_partner}' AND receiver = '{user}';")

        self.exec(f"""UPDATE messages SET read_status = 'read' WHERE sender = '{chat_partner}' AND receiver = '{user}' AND read_status = 'unread';""")

        return self.exec(f"""   SELECT 
                                message,
                                sender,
                                read_status,
                                unix_timestamp,
                                message_id
                                FROM messages 
                                WHERE sender = '{user}' 
                                AND receiver = '{chat_partner}' 
                                AND NOT read_status = 'deleted'
                                OR sender = '{chat_partner}' 
                                AND receiver = '{user}' 
                                AND NOT read_status = 'deleted'
                                ORDER BY unix_timestamp;""")

    def load_group_chat_history(self, group):

        return self.exec(f"""   SELECT 
                                message,
                                sender
                                FROM group_chat 
                                WHERE group_chat = '{group}' 
                                ORDER BY group_message_id;""")

    def is_message_read(self, message_id):

        return self.exec(f"""   SELECT
                                read_status
                                FROM messages
                                WHERE message_id = '{message_id}' 
                                """)[0][0] == "read"

    def delete_message(self, message_id, sender):

        self.exec(f"""  UPDATE 
                        messages
                        SET read_status = 'deleted'
                        WHERE message_id = '{message_id}'
                        AND sender = '{sender}';
                    """)

        return self.exec(f"""
                            SELECT 
                            read_status 
                            FROM messages
                            WHERE message_id = '{message_id}';
                            """)[0][0] == "deleted"

    def edit_message(self, message_id, new_text):

        self.exec(f"""
                        UPDATE
                        messages
                        SET message = '{new_text}'
                        WHERE 
                        message_id = '{message_id}';
                        """)

        return self.exec(f"""
                            SELECT 
                            message 
                            FROM messages
                            WHERE message_id = '{message_id}';
                            """)[0][0] == new_text

    def get_message_id(self, sender, receiver, message, timestamp):

        return self.exec(f"""   SELECT
                                message_id
                                FROM messages
                                WHERE sender = '{sender}' 
                                AND receiver = '{receiver}'
                                AND message = '{message}'
                                AND unix_timestamp = '{timestamp}'
                                LIMIT 1;
                                """)[0][0]

    # Diskussionsforum
    def create_discussion(self, title: str, text: str, author: str, creation_date: str, category: str):
        query = f"""
        INSERT INTO SEP.discussions (title, text, author, creation_date, category)
        VALUES ('{title}', '{text}', '{author}', '{creation_date}', '{category}');
        """
        self.exec(query)

        # Get the ID of the discussion that was just inserted
        return self.exec("SELECT LAST_INSERT_ID()")[0][0]

    def get_all_discussions(self):
        result = self.exec("""SELECT * FROM SEP.discussions""")
        discussions = []
        for row in result:
            discussions.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'creation_date': row[3],
                'category': row[4]
            })
        return discussions

    def get_discussion(self, discussion_id: int):

        return self.exec(f"""SELECT * FROM SEP.discussions WHERE id = {discussion_id}""")

    def get_discussion_posts(self, diskussion_id: int):

        return self.exec(f"""SELECT * FROM SEP.posts WHERE discussion_id = {diskussion_id}""")

    def get_discussion_likes(self, diskussion_id: int):

        return self.exec(f"""SELECT * FROM SEP.likes WHERE discussion_id = {diskussion_id}""")

    def get_like_by_user_and_discussion(self, user_id: str, discussion_id: int):
        # Diese Funktion überprüft, ob ein bestimmter Benutzer bereits ein "Like" für eine bestimmte Diskussion gegeben hat.
        result = self.exec(f"""SELECT * FROM SEP.likes WHERE user_id = '{user_id}' AND discussion_id = {discussion_id}""")
        return result

    def remove_like(self, user_id: str, discussion_id: int):
        # Diese Funktion entfernt ein "Like" von einem bestimmten Benutzer für eine bestimmte Diskussion.
        self.exec(f"""DELETE FROM SEP.likes WHERE user_id = '{user_id}' AND discussion_id = {discussion_id}""")

    def add_like(self, user_id: str, discussion_id: int):
        # Diese Funktion fügt ein "Like" von einem bestimmten Benutzer für eine bestimmte Diskussion hinzu.
        self.exec(f"""INSERT INTO SEP.likes (user_id, discussion_id) VALUES ('{user_id}', {discussion_id});""")

    def create_post(self, discussion_id, content, author, date):

        self.exec(f"""
                    INSERT INTO posts (discussion_id, author, date, content) VALUES 
                    ('{discussion_id}', '{author}', '{date}', '{content}');
                    """)

    def get_bookmark_by_user_and_discussion(self, user_id: str, discussion_id: int):
        '''
        Diese Funktion sucht nach Lesezeichen dieser Diskussion und des Nutzers basierend auf den Nutzernamen und der Diskussions-ID
        :param user_id: Der Nutzer nach dem wir suchen
        :param discussion_id: Die Diskussions-ID der Diskussion nach der wir suchen
        :return: Rückgabewert ist vorhanden falls Leseichen vorhanden ist
        '''
        result = self.exec(
            f"""SELECT * FROM SEP.bookmarks WHERE user_id = '{user_id}' AND discussion_id = {discussion_id}""")
        return result

    def remove_bookmark(self, user_id: str, discussion_id: int):
        # Diese Funktion entfernt ein "Like" von einem bestimmten Benutzer für eine bestimmte Diskussion.
        self.exec(f"""DELETE FROM SEP.bookmarks WHERE user_id = '{user_id}' AND discussion_id = {discussion_id}""")

    def add_bookmark(self, user_id: str, discussion_id: int):
        # Diese Funktion fügt ein "Like" von einem bestimmten Benutzer für eine bestimmte Diskussion hinzu.
        self.exec(f"""INSERT INTO SEP.bookmarks (user_id, discussion_id) VALUES ('{user_id}', {discussion_id});""")

    def get_discussion_bookmarks(self, diskussion_id: int):

        return self.exec(f"""SELECT * FROM SEP.bookmarks WHERE discussion_id = {diskussion_id}""")

    def delete_reply(self, post_id):

        return self.exec(f"""DELETE FROM SEP.posts WHERE id = '{post_id}';""")