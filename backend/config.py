from mysql_utils import MySqlUtils
import time
import json

print("Waiting...")
time.sleep(22)
print("Starting...")

path_to_run_configuration = "./run_configuration.json"

with open(path_to_run_configuration, 'r') as config_file:
    json_data = json.load(config_file)


# Set up MySQL-Table (user_data)
try:
    db = MySqlUtils(json_data['dataserver_ip'], json_data['dataserver_port'], json_data['dataserver_uname'], json_data['dataserver_password'], json_data['dataserver_database'])
    #db = MySqlUtils("127.0.0.1", 3306, "root", "1234", "SEP")
    db.exec("""CREATE TABLE SEP.user_data 
                (vorname TEXT NOT NULL COMMENT 'Vorname des Nutzers' , 
                nachname TEXT NOT NULL COMMENT 'Nachname des Nutzers' , 
                geburtsdatum TEXT NOT NULL COMMENT 'Geburtsdatum des Nutzers' , 
                email TEXT NOT NULL COMMENT 'E-Mail des Nutzers' , 
                passwort TEXT NOT NULL COMMENT 'Passwort des nutzers' , 
                2_fa_code TEXT NOT NULL COMMENT 'Ständig ändernder 2-Faktor-Code' , 
                rechte TEXT NOT NULL COMMENT 'Rechte des users (Admin / User)' , 
                profilbild TEXT NOT NULL COMMENT 'Verweis auf den Namen (id) des Profilbildes', 
                lieblingsdaten TEXT NOT NULL COMMENT 'Lieblingsdatensätze' ) ENGINE = InnoDB COMMENT = 'Tabelle mit den Nutzerdaten der SEP Software';""")

    db.exec("""CREATE TABLE SEP.support_tickets (
              ticket_id INT NOT NULL AUTO_INCREMENT COMMENT 'Ticket ID',
              ticket_name TEXT NOT NULL COMMENT 'Ticketname',
              short_desc TEXT NOT NULL COMMENT 'Kurze Beschreibung des Problems',
              long_desc TEXT NOT NULL COMMENT 'Ausführliche Beschreibung',
              creator TEXT NOT NULL COMMENT 'Verfasser des Problems',
              status TEXT NOT NULL COMMENT 'Aktueller Bearbeitungsstatus',
              PRIMARY KEY (ticket_id)
            ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Tabelle mit den Supporttickets der SEP Software';""")

    db.exec("""CREATE TABLE SEP.freunde (
              entry_id INT NOT NULL AUTO_INCREMENT COMMENT 'Eintrag ID',
              email_id TEXT NOT NULL COMMENT 'Email',
              friend_email_id TEXT NOT NULL COMMENT 'Email des Freundes',
              status TEXT NOT NULL COMMENT 'Status der Freundschaft',
              action_timestamp TEXT NOT NULL COMMENT 'UNIX-Zeit des letzten Statusänderung',
              PRIMARY KEY (entry_id)
            ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Tabelle mit den Freunden der SEP Software';""")

    db.exec("""CREATE TABLE SEP.freundesichtbarkeit (
                  email_id TEXT NOT NULL COMMENT 'Email',
                  sichtbarkeit TEXT NOT NULL COMMENT 'Sichtbarkeit'
                ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Tabelle mit den Sichtbarkeiten der Freundesliste der SEP Software';
            """)

    db.exec("""CREATE TABLE SEP.profilsichtbarkeit (
                      email_id TEXT NOT NULL COMMENT 'Email',
                      sichtbarkeit TEXT NOT NULL COMMENT 'Sichtbarkeit'
                    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Tabelle mit den Sichtbarkeiten der Freundesliste der SEP Software';
                """)

    db.exec("""CREATE TABLE SEP.messages (
                      message_id INT NOT NULL AUTO_INCREMENT COMMENT 'MESSAGE ID',
                      sender TEXT NOT NULL COMMENT 'Message sender',
                      receiver TEXT NOT NULL COMMENT 'Message receiver',
                      message TEXT NOT NULL COMMENT 'Message',
                      read_status TEXT NOT NULL COMMENT 'Has the message been read?',
                      unix_timestamp TEXT NOT NULL COMMENT 'Unix time of Message',
                      PRIMARY KEY (message_id)
                    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Tabelle mit den Sichtbarkeiten der Freundesliste der SEP Software';
                """)

    db.exec("""CREATE TABLE SEP.group_chat (
                          group_message_id INT NOT NULL AUTO_INCREMENT COMMENT 'MESSAGE ID',
                          sender TEXT NOT NULL COMMENT 'Message sender',
                          group_chat TEXT NOT NULL COMMENT 'Group (receiver)',
                          message TEXT NOT NULL COMMENT 'Message',
                          PRIMARY KEY (group_message_id)
                        ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Tabelle mit den Sichtbarkeiten der Freundesliste der SEP Software';
                    """)

except Exception as e:
    print(e)
    print("\n[ Error ]: Something went wrong. Take a closer look a the given error message above.")
    print("You might want to check the credentials.")

try:
    db = MySqlUtils(json_data['dataserver_ip'], json_data['dataserver_port'], json_data['dataserver_uname'], json_data['dataserver_password'], json_data['dataserver_database'])

    db.exec("""CREATE TABLE SEP.discussions (
              id INT NOT NULL AUTO_INCREMENT COMMENT 'Discussion ID',
              title TEXT NOT NULL COMMENT 'Discussion title',
              author TEXT NOT NULL COMMENT 'Author of the discussion',
              text TEXT NOT NULL COMMENT 'Text of the discussion',
              creation_date TEXT NOT NULL COMMENT 'Creation date of the discussion',
              category TEXT NOT NULL COMMENT 'Category of the discussion',
              PRIMARY KEY (id)
            ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Table for discussions';""")

    db.exec("""CREATE TABLE SEP.posts (
              id INT NOT NULL AUTO_INCREMENT COMMENT 'Post ID',
              discussion_id INT NOT NULL COMMENT 'Discussion ID the post belongs to',
              author TEXT NOT NULL COMMENT 'Author of the post',
              date TEXT NOT NULL COMMENT 'Date of the post',
              content TEXT NOT NULL COMMENT 'Content of the post',
              PRIMARY KEY (id),
              FOREIGN KEY (discussion_id) REFERENCES SEP.discussions(id)
            ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Table for posts';""")

    db.exec("""CREATE TABLE SEP.likes (
              id INT NOT NULL AUTO_INCREMENT COMMENT 'Like ID',
              discussion_id INT NOT NULL COMMENT 'Discussion ID the like belongs to',
              user_id TEXT NOT NULL COMMENT 'User who liked the discussion',
              PRIMARY KEY (id),
              FOREIGN KEY (discussion_id) REFERENCES SEP.discussions(id)
            ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Table for likes';""")

except Exception as e:
    print(e)
    print("\n[ Error ]: Something went wrong. Take a closer look a the given error message above.")
    print("You might want to check the credentials.")

try:
    db = MySqlUtils(json_data['dataserver_ip'], json_data['dataserver_port'], json_data['dataserver_uname'], json_data['dataserver_password'], json_data['dataserver_database'])

    db.exec("""CREATE TABLE SEP.bookmarks (
              id INT NOT NULL AUTO_INCREMENT COMMENT 'bookmark ID',
              discussion_id INT NOT NULL COMMENT 'Discussion ID the bookmark belongs to',
              user_id TEXT NOT NULL COMMENT 'User who bookmarked the discussion',
              PRIMARY KEY (id),
              FOREIGN KEY (discussion_id) REFERENCES SEP.discussions(id)
            ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'Table for likes';""")

except Exception as e:
    print(e)
    print("\n[ Error ]: Something went wrong. Take a closer look a the given error message above.")
    print("You might want to check the credentials.")

# Starting the Webserver
try:
    import app
    print("### Starting Webserver ###")
    app.start()

except Exception as e:
    print(e)
    print("Something went wrong.")

