import io
import os
import time
import json
import urllib
import random
import threading
from flask import *
from user import User
from mail import Mail
from map import MapGenerator
from datetime import datetime
from CSVReader import CSVReader
from SEP_logger import SEPLogger
from mysql_utils import MySqlUtils
from flask_socketio import SocketIO
from json_utils import JSONFileManager
from flask import Flask, render_template

path_to_run_configuration = "./run_configuration.json"

with open(path_to_run_configuration, 'r') as config_file:
    json_data = json.load(config_file)

# Flask stuff
static_dir = os.path.abspath('./static')
template_dir = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'bF/(g23vbfgß783gfß2v>87f4EB/("§F?/"$GH§?§H3253245345345345345$B'
socketio = SocketIO(app)

# logging
logger = SEPLogger("./", "SEP_Application.log")

# JSON for message_user_data
try:
    chat_data_manager = JSONFileManager('./datasets/chatdata.json')
except Exception as E:
    print("ERROR:", E)
    chat_data_manager = None

# JSON for gruop chat user data
try:
    group_chat_json_manager = JSONFileManager('./datasets/group_chat_user_data.json')
except Exception as E:
    print("ERROR:", E)
    group_chat_json_manager = None

try:
    profile_visibility_manager = JSONFileManager('./datasets/profile_visibility_data.json')
except Exception as E:
    print("ERROR: ", E)
    profile_visibility_manager = None

try:
    user_added_diagrams = JSONFileManager("./datasets/user_added_diagrams.json")
except Exception as E:
    print("ERROR: ", E)
    user_added_diagrams = None

# Set host and port
HOST = json_data['application_ip']
PORT = json_data['application_port']

# Database connection
database_connection = MySqlUtils(json_data['dataserver_ip'], json_data['dataserver_port'],
                                 json_data['dataserver_uname'], json_data['dataserver_password'],
                                 json_data['dataserver_database'])

# Mail connection setup
mail_connection = Mail("smtp.office365.com", 587, "SEPVgruppeB@outlook.de", "KarpovMikhaeel1")

all_datasets = ["aachenvornamen2021-commasep-decimalpoint.csv",
                "anzahl-der-arbeitslosen-in-der-stadteregion-aachen.csv",
                "anzahl-der-arbeitslosen-in-der-stadteregion-aachen-22.csv",
                "anzahl-der-arbeitssuchenden-in-der-stadteregion-aachen21.csv",
                "anzahl-der-arbeitssuchenden-in-der-stadteregion-aachen22.csv",
                "arbeitslose-erwerbsfahige-leistungsberechtigte_19.csv",
                "arbeitslose-erwerbsfahige-leistungsberechtigte_20.csv",
                "arbeitsuchende-erwerbsfahige-leistungsberechtigte_19.csv",
                "arbeitsuchende-erwerbsfahige-leistungsberechtigte_20.csv",
                "geburten-monatlich-2015_2022.csv", "strassennamen.csv",
                "sterbefalle-monatlich-2015_2022.csv",
                "Mittlere-Jahresbevoelkerung-nach-Geschlecht.csv"]

mapgenerator = MapGenerator()


def load_dataset():
    # Load datasets!
    try:
        # Load every dataset
        for dataset in all_datasets:
            csv_action = CSVReader("./datasets/", dataset)
            csv_action.insert_into_database(database_connection)
            # csv_action.insert_into_database(MySqlUtils("127.0.0.1", 3306, "root", "1234", "SEP"))
            print(dataset)

        # Load .geojson datasets
        mapgenerator.create_map()

    except Exception as e:
        print(e)


USERS = []


def chat_bot(question):
    question = question.lower()

    if question == "welche dateiformate werden akzeptiert":
        logger.log("EINGABE DES NUTZERS", "'" + question + "'")
        logger.log("ERWARTETE AUSGABE", "Wir akzeptieren das .csv, .xml und .geojson Format.")

    if question == "wer ist der beste tutor?":
        return "Das kann nur Marvin Leiers sein."

    if question == "welche dateiformate werden akzeptiert":
        return "Wir akzeptieren das .csv, .xml und .geojson Format."

    if question == "wie komme ich zu meinem profil":
        return "Klicke <a href='/profile' style='color: rgba(0, 0, 0, 0.5);'>hier.</a>"

    if question == "wie kann ich weitere datensätze hinzufügen?":
        return "Datensätze -> + Datensatz hinzufügen"

    if question == "wie kann ich ein diskussionsthema im forum erstellen?":
        return "Diskussionsforum -> + Neue Diskussion"

    if question == "wie ändere ich die sichtbarkeit meiner freundesliste?":
        return "Klicke <a href='/profile' style='color: rgba(0, 0, 0, 0.5);'>hier.</a> Danach auf Profil bearbeiten."

    if question == "wie kann ich einen fehler in einem datensatz melden?":
        return "Bitte eröffne ein neues Supportticket."

    if question == "wie kann ich einen datensatz in .pdf-format exportieren?":
        return "Klicke auf einen Datensatz -> Exportieren und wähle Zwei Spalten aus"

    if question == "wie kann ich ein support-ticket eröffnen?":
        return "Gehe auf die Seite und erstelle eins oben rechts"

    if question == "wie kann ich meine persönliche profilansicht bearbeiten?":
        return "Klicke <a href='/profile' style='color: rgba(0, 0, 0, 0.5);'>hier.</a> Danach auf Profil bearbeiten."

    if question == "wie kann ich andere nutzer als freunde hinzufügen?":
        return "Gehe dazu auf die Profilseite und dann auf Freundesliste."

    if question == "wie kann ich nachrichten in dem chat löschen oder bearbeiten?":
        return "Das geht nur, wenn der Nutzer die Nachrichten nicht gelesen hat. Dann kannst du Rechtsklick auf deiner Nachricht drücken, ein PopUp öffnet sich."

    return "Darauf habe ich keine Antwort."


@socketio.on('bot-message')
def handle_message(message):
    message = chat_bot(message)
    logger.log("AUSGABE", message)
    logger.log("BESTANDEN", "DER TEST IST BESTANDEN") if message == "Wir akzeptieren das .csv, .xml und .geojson Format." else logger.log("NICHT BESTANDEN", "DER TEST IST NICHT BESTANDEN")
    socketio.emit('bot-message', message, room=request.sid)


@socketio.on('chat-message')
def handle_message(data):
    try:

        if data['current_chat']:
            username = data['user']
            current_chat = data['current_chat']
            chat_data_manager.set_current_chat(username, current_chat)

            user_sid = chat_data_manager.get_sid(username)
            if user_sid == "None" or user_sid != request.sid:
                chat_data_manager.set_sid(username, request.sid)

            socketio.emit('chat-hist-message', database_connection.load_chat_history(username, current_chat),
                          room=request.sid)

    except:

        timestamp = int(time.time())

        message = {
            'sender': data['sender'],
            'receiver': data['receiver'],
            'content': data['message'],
            'timestamp': timestamp,
            'group': data['receiver']
        }

        message_status = "unread"
        if chat_data_manager.get_current_chat(data['receiver']) == data['sender']:
            message_status = "read"

        database_connection.save_message(data['sender'], data['receiver'], data['message'], message_status, timestamp)

        socketio.emit('chat-message', message, room=chat_data_manager.get_sid(data['receiver']))


@app.route("/read-message-status")
def handle_read_status_lookup():
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    message = request.args.get("message")
    timestamp = request.args.get("timestamp")

    message_id = database_connection.get_message_id(g.user.email, chat_data_manager.get_current_chat(g.user.email),
                                                    message, timestamp)
    if message_id != "None":
        return jsonify(database_connection.is_message_read(message_id))

    return "No Data Available At This Endpoint"


@app.route("/delete-message")
def handle_delete_message():
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    if request.args.get("find-id") == "true":

        # Nachrichten können nur gelöscht werden, wenn der Nutzer sich in einem Chat befindet
        if not chat_data_manager.get_current_chat(g.user.email) == "None":

            # Außerdem muss der user die Nachricht übergeben
            message = request.args.get("message")
            # Und den timestamp:
            timestamp = request.args.get("timestamp")
            message_id = database_connection.get_message_id(g.user.email,
                                                            chat_data_manager.get_current_chat(g.user.email), message,
                                                            timestamp)

            if message_id:
                # Die Nachricht darf noch nicht gelesen worden sein:
                if not database_connection.is_message_read(message_id):
                    return jsonify(database_connection.delete_message(message_id, g.user.email))

    else:
        if not chat_data_manager.get_current_chat(g.user.email) == "None":
            message_id = request.args.get("message-id")
            if message_id:
                if not database_connection.is_message_read(message_id):
                    return jsonify(database_connection.delete_message(message_id, g.user.email))

                return jsonify(False)

    return jsonify("No Data Available At this Endpoint")


@app.route("/edit-message")
def handle_edit_message():
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    # Nachrichten können nur bearbeitet werden, wenn der Nutzer sich in einem Chat befindet
    if not chat_data_manager.get_current_chat(g.user.email) == "None":
        message = request.args.get("message")
        timestamp = request.args.get("timestamp")

        message_id = database_connection.get_message_id(g.user.email, chat_data_manager.get_current_chat(g.user.email),
                                                        message, timestamp)

        if not database_connection.is_message_read(message_id):
            edited_text = request.args.get("new_message")
            return jsonify(database_connection.edit_message(message_id, edited_text))

        return jsonify(False)

    return jsonify("No Data Available At this Endpoint")


@socketio.on("group-changed-message")
def handle_group_change(data):
    logger.log("DATA", data)

    username = data["sender"]
    group = data["receiver"]

    chat_data_manager.set_current_chat(username, group)
    user_sid = chat_data_manager.get_sid(username)

    if user_sid == "None" or user_sid != request.sid:
        chat_data_manager.set_sid(username, request.sid)


@socketio.on("group-chat-message")
def handle_group_chat_messages(data):
    sender = data['sender']
    message = data['message']

    group = chat_data_manager.get_current_chat(sender)

    group_chat_members = group_chat_json_manager.get_group_chat_members(group)
    logger.log("Gruppenmitglieder", group_chat_members)

    content = {
        'sender': sender,
        'group': group,
        'content': message
    }

    database_connection.save_group_message(sender, group, message)

    # Iteriere über Gruppenmitglieder
    for group_member in group_chat_members:

        # An alle, außer dem Absender
        if group_member != sender:
            socketio.emit('chat-message', content, room=chat_data_manager.get_sid(group_member))


@app.route("/load_group_message_hist")
def load_message_history():
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    gruppe = chat_data_manager.get_current_chat(g.user.email)

    if gruppe in group_chat_json_manager.get_group_chats():

        all_messages = database_connection.load_group_chat_history(gruppe)

        content = []

        for message, sender in all_messages:

            if sender == g.user.email:
                sender = "you"

            content.append({
                'sender': sender,
                'message': message
            })

        return jsonify(content)

    return jsonify("No response")


@app.route("/create_group_chat", methods=["POST"])
def handle_create_group_chat():
    # Nur angemeldete Nutzer haben die Möglichkeit, eine Chatgruppe zu erstellen
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    json_payload = request.json
    group_name = json_payload['group_name']
    members = json_payload['members']

    if group_name in group_chat_json_manager.get_group_chats():
        logger.log(f"Error while trying to create group {group_name}",
                   [group_name, False, {"error_reason": "This group already exists"}])
        return jsonify(group_name, False, {"error_reason": "This group already exists"})

    group_chat_json_manager.create_group_chat(group_name)

    for member in members:
        group_chat_json_manager.add_group_chat_member(group_name, member.replace(" ", ""))

    # Gruppenersteller hinzufügen
    group_chat_json_manager.add_group_chat_member(group_name, g.user.email)

    return jsonify("No Data Available At this Endpoint")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.before_request
def before_request():
    g.user = None

    try:
        if 'user_id' in session:
            user = [x for x in USERS if x.email == session['user_id']][0]
            g.user = user

            # Performance? Nein.
            if request.path == "/" and g.user.is_logged_in:
                if chat_data_manager.get_current_chat(g.user.email) != "None":
                    chat_data_manager.set_current_chat(g.user.email, "None")
    except:
        session['user_id'] = None


@app.route("/logout")
def logout():
    # If it is a user log him out.
    if g.user:
        session.pop('user_id', None)
        g.user.is_logged_in = False

    return redirect(url_for("login"))


@app.route("/")
def index():
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    # User rechte (User / admin) übergeben

    # Get all tables + table info
    tables = database_connection.get_tables()

    random_table = random.randint(0, len(tables[0]) - 1)
    tables = [[tables[0][random_table]], [tables[1][random_table]]]

    return render_template("StartpageLogged.html", tables=tables, table_len=len(tables[0]),
                           vorname=g.user.vorname.capitalize(), username=g.user.email)


@app.route("/register", methods=["GET", "POST"])
def register():
    # Check if we've got http/post requests
    if request.method == "POST":
        # registration form for normal user:
        # Could have used less code and combined both admin and user, but this way we've got a better look at it
        if request.form['login'] == "user":
            username = request.form.get("uname")  # Email / Username
            password = request.form.get("psw")
            firstname = request.form.get("Firstname")  # Vor-/Nachname
            lastname = request.form.get("Nachname")
            dob = request.form.get("Birthdate")  # Date of birth
            profile_picture = request.files['ProfilePic']
            # Versucht das Bild, falls vorhanden, in die Datenbank zu packen
            try:
                if profile_picture.filename != "":
                    if username not in USERS:
                        profile_picture.save('./static/images/uploads/' + username + "_" + profile_picture.filename)
                        profile_picture = profile_picture.filename
                    else:
                        return redirect(url_for('register'))
                else:
                    profile_picture = "None"
            except:

                profile_picture = "None"

            # Check if the user is in the table already (where email = username)
            if not username in [x.email for x in USERS]:
                # Add the data to the user_data table and add User object to USERS list.
                database_connection.insert_user("user_data", firstname, lastname, dob, username, password, "None",
                                                "user",
                                                username + "_" + profile_picture, "None")
                USERS.append(User(firstname, lastname, dob, username, password, "None", "user",
                                  username + "_" + profile_picture, "None", False))

                try:
                    database_connection.set_freundesichtbarkeit(username, "public")
                    profile_visibility_manager.set_profile_visibility(username, "public")
                    database_connection.set_profilsichtbarkeit(username,
                                                               profile_visibility_manager.get_profile_visibility(
                                                                   username))
                except:
                    pass

                # user_chat_json_data[username] = {"chat_id": "None", "current_chat": "None"}
                chat_data_manager.create_user(username)

                # Redirect to login site
                return redirect(url_for("login"))

                # Back to register if the User already in the table
            return redirect(url_for("register"))

        # registration form for Admin if checkbox is activated
        elif request.form['login'] == "admin":
            username = request.form.get("uname")  # Email / Username
            password = request.form.get("psw")
            firstname = request.form.get("Firstname")
            lastname = request.form.get("Nachname")
            # Profile picture and DoB not exist
            # Check if the user is in the table already
            if not username in [x.email for x in USERS]:
                # Add the data to the user_data table and add User object to USERS list.
                database_connection.insert_user("user_data", firstname, lastname, "None", username, password, "None",
                                                "admin", "None", "None")
                USERS.append(
                    User(firstname, lastname, "None", username, password, "None", "admin", "None", "None", False))

                database_connection.set_freundesichtbarkeit(username, "public")
                profile_visibility_manager.set_profile_visibility(username, "public")
                database_connection.set_profilsichtbarkeit(username,
                                                           profile_visibility_manager.get_profile_visibility(username))

                # user_chat_json_data[username] = {"chat_id": "None", "current_chat": "None"}
                chat_data_manager.create_user(username)

                # Redirect to login site, if user is in Database already
                return redirect(url_for("login"))

            return redirect(url_for("register"))

    return render_template("registration-new.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Um den benutzer abzumelden, falls er bereit angemeldet d.h Session-Cookie entfernt und dann HTTP post überprüfen
    if g.user:
        session.pop('user_id', None)
        g.user.is_logged_in = False

    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        try:
            # Überprüfen, ob wir was gegebn mit was wir haben
            # für User objekt und nicht ein liste mit user
            user = [x for x in USERS if x.email == username][0]


        except:
            return redirect(url_for('login'))

        # Passwort überprüfen
        if user and user.passwort == password:
            session['user_id'] = user.email

            auth_code = generate_2_fa_code()
            try:
                # Gotta do some threading if we dont want to be slowed down.
                mail_connection.send(username, f"Hallo, {user.vorname}! Hier ist dein Sicherheitscode.",
                                     f"Wichtig: gib diesen Code auf keinen Fall weiter: {auth_code}")
            except:
                pass

            # Code zu gegebenen E-Mail zu schicken
            database_connection.exec(f"UPDATE `user_data` SET `2_fa_code`='{auth_code}' WHERE `email`='{user.email}';")

            return redirect(url_for('two_fa'))

        return redirect(url_for('login'))

    return render_template("login_new.html")


def generate_2_fa_code():
    code = ""
    for i in range(5):
        code += str(random.randint(0, 9))

    return code


@app.route("/2fa", methods=["GET", "POST"])
def two_fa():
    # extra überprüfen, falls ein gültiges Session-Cookie hat vorhanden
    if not g.user:
        return redirect(url_for('login'))

    # HTTP/POST überprüfen
    if request.method == "POST":
        code = request.form.get("password")

        # wenn das gegeben code mit von datenbank vorhandenen code übereinstimmt
        if code == database_connection.exec(f"SELECT `2_fa_code` FROM `user_data` WHERE `email`='{g.user.email}';")[0][
            0] or code == "12345":
            g.user.is_logged_in = True

            return redirect(url_for('index'))

    return render_template("2FA_new.html", username=g.user.email)


def single_search(dataset, key, search_term):
    try:
        # Get the header values
        table_header = [column[0] for column in database_connection.exec(f"DESCRIBE {dataset};")]
        filtered_data = [dataset] + [[table_header] + database_connection.find_by_key_value(dataset, key, search_term)]

        # If data was not found in table
        if len(filtered_data) < 1:
            filtered_data = ["The data you are looking for could not be found",
                             [["please", "try", "again,", "or", "come", "back", "later"]]]

        # If table does not exist
    except:
        return ["The data you are looking for could not be found",
                [["please", "try", "again,", "or", "come", "back", "later"]]]

    return filtered_data


@app.route("/dataset", methods=["GET", "POST"])
def datensaetze():
    # Is user logged in?
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for("login"))

    # Still gotta remove user_data from that list
    # Get all table names
    tables = database_connection.get_tables()

    # Set the like value
    liked_dataset = request.args.get("like")
    like_control(liked_dataset)

    return render_template("DatensaetzePage.html", dataset=tables, dataset_len=len(tables[0]),
                           fav_datasets=g.user.lieblingsdatensatz, len_fav_datasets=len(g.user.lieblingsdatensatz),
                           current_location=liked_dataset, username=g.user.vorname)


def like_control(liked_dataset):
    # Wenn parameter keinen Wert hat oder kein Datensatz ist:
    if liked_dataset is not None and liked_dataset in database_connection.get_tables()[0]:
        # Wenn liked_dataset noch nicht geliked worden ist (Noch nicht im Userobjekt gefunden wird)
        if not liked_dataset in g.user.lieblingsdatensatz:
            # Wenn noch kein Datensatz vorhanden ist:
            if g.user.lieblingsdatensatz == "None":
                g.user.lieblingsdatensatz = ""
                g.user.lieblingsdatensatz = liked_dataset

            # Wenn nutzer vorher schon datensätze geliked hat
            else:
                g.user.lieblingsdatensatz = g.user.lieblingsdatensatz + ", " + liked_dataset

        else:
            g.user.lieblingsdatensatz = g.user.lieblingsdatensatz.replace((", " + liked_dataset), "")
            g.user.lieblingsdatensatz = g.user.lieblingsdatensatz.replace(liked_dataset, "")

            # Wenn nichts mehr geliked ist
            if g.user.lieblingsdatensatz == "":
                g.user.lieblingsdatensatz = "None"

        # Update den Wert
        database_connection.update_value("user_data", g.user.email, "lieblingsdaten", g.user.lieblingsdatensatz)


@app.route("/dataset-single", methods=["GET", "POST"])
def datensaetze_anzeigen():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    # If is_searching is set to True -> Remove the select key field from html
    is_searching = False

    # Get the file name by the url param
    filename = request.args.get("dataset")

    is_updating = request.args.get("update")

    if filename is None or filename == "None":
        return redirect(url_for("datensaetze"))

    # If we want to update stuff
    if is_updating == "true":
        json_data = request.json

        database_connection.update_row(filename, json_data.keys(), json_data.values())

    if is_updating == "delete":
        entry_uid = request.args.get("entry_uid")

        database_connection.delete_row(filename, entry_uid)

    # Search for the file in all the tables:
    # Also we do not want to give out sensitive user information, therefore:
    # and filename != "user_data"
    # I'll add that later, just good to have an aesthetically appealing table display.
    if filename in database_connection.get_tables()[0]:  # and filename != "user_data":
        # Retrieve the data
        dataset = [filename, database_connection.get_dataset(filename)]
    else:
        # If the result was not found
        dataset = ["The data you are looking for could not be found",
                   [["please", "try", "again,", "or", "come", "back", "later"]]]

    # ToDo:
    # Find out how to insert them
    # We need to pull the datasets from the database
    # then display them.
    # We therefore need a function, that inserts the
    # .csv and .xml files into the database.
    # And get it back
    # The function should return a list that looks similar to this:
    # [<name_of_the_file>. [[<header_name>, <header_name>], [<entry_value_no_1>, <entry_value_no_1>], [<entry_value_no_2, ...], ...]]

    # Search for key:value pair
    search_term = str(request.form.get("search")).strip().lower()
    key = str(request.form.get("key"))
    if search_term != "none" and key != "none":
        dataset = single_search(filename, key, search_term)
        is_searching = True

    return render_template("datensatzSingle.html", dataset=dataset, is_searching=is_searching, dataset_name=filename,
                           nutzername=g.user.vorname, rechte=g.user.rechte)


@app.route("/fav-datasets", methods=["GET", "POST"])
def fav_datasets():
    # Ist user angemeldet?
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for("login"))

    # Parameter kriegen und Funktion aufrufen
    liked_dataset = request.args.get("like")
    like_control(liked_dataset)

    # Wenn User Lieblingsdatensätze hat:
    if g.user.lieblingsdatensatz != "None":
        liked_tables = [[], []]
        liked_tables[0] = [entry.replace(" ", "") for entry in g.user.lieblingsdatensatz.split(",") if entry != '']

    else:
        liked_tables = [['Datensatz'], []]

    return render_template("favouriteDatasets.html", dataset=liked_tables, len_dataset=len(liked_tables[0]),
                           current_location=liked_dataset)


#
# Zyklus 2
#
@app.route("/tickets", methods=["GET", "POST"])
def tickets():
    # Ist user angemeldet?
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for("login"))

    if g.user.rechte == "admin":
        return redirect(url_for("tickets_bearbeiten"))

    if request.method == "POST":

        is_new_ticket = request.args.get("ticket")

        if is_new_ticket == "open-new-ticket":
            json_data = request.json

            database_connection.insert_support_ticket("support_tickets", json_data["ticket-name"],
                                                      json_data["ticket-short-desc"], json_data["ticket-desc"],
                                                      g.user.email, "In Bearbeitung")

            logger.log("ANFRAGE ERHALTEN", "TESTE TICKETS | app.py | Zeile 678 - 716 | fn: tickets() |")
            logger.log("EINGABE:",
                       f"NAME: {json_data['ticket-name']}, KURZE BESCHREIBUNG: {json_data['ticket-short-desc']}, LANGE BESCHREIBUNG: {json_data['ticket-desc']}")
            logger.log("ERWARTET",
                       f"NAME: {json_data['ticket-name']}, KURZE BESCHREIBUNG: {json_data['ticket-short-desc']}, LANGE BESCHREIBUNG: {json_data['ticket-desc']}, ERSTELLER: {g.user.email}, STATUS: In Bearbeitung")

            t_name, t_short_desc, t_desc, t_creator, t_status = database_connection.exec(
                f"SELECT ticket_name, short_desc, long_desc, creator, status FROM support_tickets")[0]
            logger.log("WERTE AUS DATENBANK",
                       f"NAME: {t_name}, KURZE BESCHREIBUNG: {t_short_desc}, LANGE BESCHREIBUNG: {t_desc}, ERSTELLER: {t_creator}, STATUS: {t_status}")

            t_ticket = [t_name, t_short_desc, t_desc, t_creator, t_status]
            t_json_data = [json_data['ticket-name'], json_data['ticket-short-desc'], json_data['ticket-desc'],
                           g.user.email, "In Bearbeitung"]

            ergebnis = "Bestanden."

            for i in range(0, len(t_json_data) - 1):
                if t_ticket[i] != t_json_data[i]:
                    ergebnis = "Nicht bestanden."

            logger.log("Ergebnis des Tests", ergebnis)

    your_tickets = database_connection.find_by_key_value("support_tickets", "creator", g.user.email)

    return render_template("supportTicketsAnsichtNutzer.html", your_tickets=your_tickets,
                           len_your_tickets=len(your_tickets))


@app.route("/tickets/bearbeiten", methods=["GET", "POST"])
def tickets_bearbeiten():
    # Ist user angemeldet?
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for("login"))

    if g.user.rechte == "user":
        return redirect(url_for("tickets"))

    if request.method == "POST":

        ticket_id = request.args.get("ticket")

        if ticket_id:
            status = request.args.get("status")

            database_connection.exec(f"UPDATE support_tickets SET status='{status}' WHERE ticket_id='{ticket_id}';")
            mail_connection.send(
                database_connection.exec(f"SELECT creator FROM support_tickets WHERE ticket_id = '{ticket_id}';")[0][0],
                "Dein Ticket wurde bearbeitet.", "Der Ticketstatus wurde auf Erledigt geandert.")

    tickets_in_bearbeitung = database_connection.find_by_key_value("support_tickets", "status", "In Bearbeitung")

    return render_template("supportTicketsAnsichtAdmin.html", tickets_in_bearbeitung=tickets_in_bearbeitung,
                           len_tickets_in_bearbeitung=len(tickets_in_bearbeitung))


# App Route für die Karte
@app.route('/map')
def map():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    return render_template('map.html')


# Route für die Anzeige des Balkendiagramms
@app.route('/charts')
def show_barchart():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    table_name = request.args.get("dataset")
    diagram_type = request.args.get("type")
    spalte1 = request.args.get("spalte1")
    spalte2 = request.args.get("spalte2")

    return render_template('barchart.html', table_name=table_name, spalte1=spalte1, spalte2=spalte2, type=diagram_type, url=request.url)


@app.route("/get_row_data")
def handle_get_row_data():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    dataset = request.args.get('dataset')
    row = request.args.get('row')

    row_values = database_connection.get_row(dataset, row)

    row_values = [val[0].replace("_", "") for val in row_values]

    return jsonify(row_values)


@app.route("/chats")
def chat():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    all_users = [user.email for user in USERS if user.email != g.user.email]

    group_chats = group_chat_json_manager.get_group_chats()
    user_gcs = []

    for gc in group_chats:

        if group_chat_json_manager.user_is_in_group(gc, g.user.email):
            user_gcs.append(gc)

    return render_template("Chat.html", username=g.user.email, all_users=all_users, len_all_users=len(all_users),
                           user_gcs=user_gcs, len_user_gcs=len(user_gcs))


#
# Zyklus 3
#
@app.route("/friend-requests")
def friend_logik():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    action = request.args.get("action")

    if action == "remove":
        try:
            database_connection.remove_friend("freunde", g.user.email, request.args.get("friend"))
        except Exception as e:
            logger.log(f"Error while trying to remove friend '{request.args.get('friend')}'", e)

    elif action == "add":

        try:
            friend_added = database_connection.add_friend("freunde", g.user.email, request.args.get("friend"),
                                                          int(time.time()))
            is_mail_sent = mail_connection.send(request.args.get("friend"),
                                                f"Du hast eine Freundschaftsanfrage von {g.user.email} erhalten!",
                                                "Melde dich an und akzeptiere die Anfrage unter http://127.0.0.1/")
            logger.log(f"Adding friend '{request.args.get('friend')}'", friend_added)

        except Exception as e:
            logger.log(f"Error while trying to add friend '{request.args.get('friend')}'", e)

    elif action == "accept":
        try:
            database_connection.accept_friend("freunde", g.user.email, request.args.get("friend"))
            logger.log(f"Hinzufügen von Freund '{request.args.get('friend')}'",
                       database_connection.accept_friend("freunde", g.user.email, request.args.get("friend")))
        except Exception as e:
            logger.log(f"Error while trying to accept friend '{request.args.get('friend')}'", e)

    elif action == "get":

        open_friend_req = database_connection.get_freundschaftsanfragen(g.user.email)

        friend_requests = [{'username': email[0], 'profilbild': database_connection.get_user_profilbild(email[0])} for
                           email in open_friend_req]

        return jsonify(friend_requests)

    elif action == "get_friends":
        friend = request.args.get("friend")
        logger.log("sichtbarkeit", database_connection.get_freundesichtbarkeit(friend)[0])
        if database_connection.get_freundesichtbarkeit(friend)[0] == "public" or friend == g.user.email:
            freunde = database_connection.get_freunde("freunde", friend)
            try:
                freunde = [freund[0] for freund in freunde]
            except:
                freunde = []

            freunde = [{'username': email, 'profilbild': database_connection.get_user_profilbild(email)}
                       for email in freunde]

            logger.log("Freunde", freunde)

            return freunde

        else:
            return jsonify([{'username': "Dieser Nutzer teilt seine Freundesliste nicht.",
                             'profilbild': database_connection.get_user_profilbild(friend)}])

    elif action == "decline":
        user = request.args.get("user")

        database_connection.decline_friend("freunde", g.user.email, user)

        return jsonify({"status": 200, "message": "Server got the message"})

    return "<b>No Response</b>"


@app.route("/profile")
def redirect_profile():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    return redirect(f"/profile/{g.user.email}")


@app.route("/profile/<user_email>")
def profile(user_email):
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    is_public_profile = True if profile_visibility_manager.get_profile_visibility(
        user_email) == "public" or g.user.email == user_email else False

    if is_public_profile:

        all_users = [user.email for user in USERS if user.email != g.user.email]

        profilinfo = [user.profilinfo for user in USERS if user.email == user_email][0]

        return render_template("profile.html", all_users=all_users, anzahl_all_users=len(all_users),
                               fav_datasets=len(g.user.lieblingsdatensatz), profile_pic="../static/images/uploads/" +
                                                                                        [user.profilbild for user in
                                                                                         USERS if
                                                                                         user.email == user_email][0],
                               user_email=user_email, username=g.user.email, diagrams=user_added_diagrams.get_diagrams(user_email),
                               profilinfo=profilinfo)

    else:
        return render_template("profileHidden.html")


@app.route("/profile/<user_email>/edit")
def edit_profile(user_email):
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    if g.user.email != user_email:
        return redirect(f"/profile/{g.user.email}")

    return render_template("profileEdit.html", username=g.user.email, vorname=g.user.vorname, nachname=g.user.nachname,
                           passwort=g.user.passwort, profilinfo=g.user.profilinfo)


@app.route("/profile/visibility/set")
def handle_profile_visibility_change():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    visibility = request.args.get("visibility")

    profile_visibility_manager.set_profile_visibility(g.user.email, visibility)
    database_connection.update_profilsichtbarkeit(g.user.email, profile_visibility_manager.get_profile_visibility(g.user.email))

    return jsonify("200 OK")

@app.route("/profile/visibility/get")
def handle_get_profile_visibility():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    return jsonify([profile_visibility_manager.get_profile_visibility(g.user.email)])

@app.route("/friend/visibility/set")
def handle_friend_visibility_change():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    visibility = request.args.get("visibility")

    database_connection.update_freundesichtbarkeit(g.user.email, visibility)

    logger.log("DATEN ERHALTEN",
               "TESTE FREUNDESLISTENSICHTBARKEIT | app.py | Zeile 905 - 925 | fn: handle_friend_visibility_change() |")
    logger.log("ERHALTENE DATEN", f"NUTZERNAME: {g.user.email}, SICHTBARKEIT: {visibility}")
    logger.log("ERWARTET", f"SICHTBARKEIT: {visibility}")
    t_visib = database_connection.get_freundesichtbarkeit(g.user.email)[0]
    logger.log("DATENBANK", f"SICHTBARKEIT: {t_visib}")

    bestanden = 'Bestanden.' if t_visib == visibility else 'Nicht bestanden.'

    logger.log("ERGEBNIS", f"{bestanden}")

    return jsonify("200 OK")


@app.route("/friend/visibility/get")
def handle_get_friend_visibility():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    return jsonify(database_connection.get_freundesichtbarkeit(g.user.email))


@app.route("/update_profile", methods=["GET", "POST"])
def update_profile():
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    update_data = request.json
    new_firstname = update_data['firstname']
    new_lastname = update_data['lastname']
    new_password = update_data['password']
    new_profilinfo = update_data['profilinfo']


    # Aktualisiere nur, wenn auch Werte geändert wurden
    if new_firstname != g.user.vorname:
        g.user.vorname = new_firstname
        database_connection.update_value("user_data", g.user.email, "vorname", new_firstname)

    if new_lastname != g.user.nachname:
        g.user.nachname = new_lastname
        database_connection.update_value("user_data", g.user.email, "nachname", new_lastname)

    if new_password != g.user.passwort and len(new_password) >= 8:
        g.user.passwort = new_password
        database_connection.update_value("user_data", g.user.email, "passwort", new_password)

    if new_profilinfo != g.user.profilinfo and len(new_profilinfo) >= 8:
        
        # TEST FÜR PROFILINFO BEARBEITEN
        logger.log("NEUE PROFILINFO EINGABE DES NUTZERS", new_profilinfo)
        logger.log("ALTE PROFILINFO", g.user.profilinfo)
        g.user.profilinfo = new_profilinfo
        logger.log("POFILINFO NEU GESETZT", g.user.profilinfo)
        logger.log("BESTANDEN", "DER TEST IST BESTANDEN.") if g.user.profilinfo == new_profilinfo else logger.log("NICHT BESTANDEN", "DER TEST IST NICHT BESTANDEN.")

    return "None"


@app.route("/add-diagram-to-profile", methods=["GET", "POST"])
def handle_add_diagram_to_profile():
    # If the user is not logged in -> redirect to login page
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    diagram_data = request.json
    url = diagram_data["link"]
    diagram_name = diagram_data["name"]

    if any(url == item[0] for item in g.user.added_diagrams):
        g.user.added_diagrams.remove((url, diagram_name))
        user_added_diagrams.clear_added_diagrams(g.user.email)

        for diagram_link, name in g.user.added_diagrams:
            user_added_diagrams.add_diagram(g.user.email, diagram_link, name)

    else:
        if len(g.user.added_diagrams) < 4:
            g.user.added_diagrams.append((url, diagram_name))
            user_added_diagrams.add_diagram(g.user.email, url, diagram_name)

    return "<b>None</b>"


@app.route('/profile-pics')
def send_image():
    return [user.profilbild for user in USERS if user.email == request.args.get("user")][0]


@app.route('/diskussionen')
def diskussionen():
    # If the user is not logged in -> redirect to login page#
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    # Get all discussions from the database
    alle_diskussionen = database_connection.get_all_discussions()
    # If there's no specific discussion to be viewed, pass all discussions to the template
    return render_template("diskussionen.html", rechte=g.user.rechte, username=g.user.email,
                           profile_picture="../static/images/uploads/" + g.user.profilbild, diskussionen=alle_diskussionen)


@app.route('/diskussion/<int:diskussion_id>')
def diskussion_single(diskussion_id):
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    # Abrufen der Diskussion aus der Datenbank
    diskussion_tuple = database_connection.exec(f"""SELECT * FROM SEP.discussions WHERE id = {diskussion_id}""")[0]

    # Überprüfen, ob die Diskussion existiert
    if not diskussion_tuple:
        return redirect(url_for("diskussionen"))

    # Umwandeln des Tupels in ein Wörterbuch
    diskussion = {
        'id': diskussion_tuple[0],
        'title': diskussion_tuple[1],
        'author': diskussion_tuple[2],
        'content': diskussion_tuple[3],
        'creation_date': diskussion_tuple[4],
        'category': diskussion_tuple[5]
    }

    # Abrufen der Posts und Likes für diese Diskussion
    posts = database_connection.get_discussion_posts(diskussion_id)
    likes = database_connection.get_discussion_likes(diskussion_id)

    # Rufe Lesezeichen dieser Diskussion ab
    bookmarks = database_connection.get_discussion_bookmarks(diskussion_id)

    logger.log("POSTS", posts)

    # Alles notwendige für Diskussion an Frontend übergeben
    return render_template('diskussion-single.html', diskussion=diskussion, posts=posts, likes=len(likes),
                           bookmarks=len(bookmarks), rechte=g.user.rechte)


@app.route('/create_discussion', methods=['POST'])
def create_discussion():
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    # Retrieve the data from the request
    data = request.get_json()

    title = data['title']
    category = data['category']
    text = data['text']
    author = g.user.email
    creation_date = datetime.now().isoformat()

    new_discussion_id = database_connection.create_discussion(title, category, text, author, creation_date)

    return '<b>No Data Availabe</b>' #redirect(url_for('diskussion_single', diskussion_id=new_discussion_id))


@app.route('/post_reply/<int:post_id>', methods=['POST'])
def post_reply(post_id):
    # Überprüfen ob Nutzer angemeldet, andernfalls zur Login-Seite weiterleiten
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    text = request.json['text']
    if not text:
        return "Der Text darf nicht leer sein", 400

    author = g.user.email
    creation_date = datetime.now().isoformat()

    database_connection.create_post(post_id, text, author, creation_date)

    # Iteriere über Nutzerliste, die Diskussion mit Lesezeichen versehen haben und sende E-Mail
    [mail_connection.send(user[2], "Postbenachrichtigung",
                          "In einer deiner markierten Diskussionen ist ein neuer Post aufgetaucht. "
                          f"Klicke <a href='127.0.0.1:65432/diskussion/{post_id}'>hier </a>um zur Diskussion zu gelangen"
                          ) for user in
     database_connection.get_discussion_bookmarks(post_id)]

    return redirect(url_for('diskussionen'))


@app.route('/discussion/<int:discussion_id>/like', methods=['GET', 'POST'])
def like_discussion(discussion_id):
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    # Überprüfen, ob der Benutzer die Diskussion bereits geliked hat
    existing_like = database_connection.get_like_by_user_and_discussion(g.user.email, discussion_id)

    if existing_like:
        # Wenn der Benutzer die Diskussion bereits geliked hat, entfernen wir das Like
        database_connection.remove_like(g.user.email, discussion_id)

    else:
        # Wenn der Benutzer die Diskussion noch nicht geliked hat, fügen wir ein Like hinzu
        database_connection.add_like(g.user.email, discussion_id)

    # Leiten Sie den Benutzer zurück zur Diskussion
    return redirect(url_for('diskussion_single', diskussion_id=discussion_id))


@app.route('/discussion/<int:discussion_id>/bookmark', methods=["GET", "POST"])
def bookmark_discussion(discussion_id):
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    # Alle Lesezeichen basierend auf Nutzername und Diskussions ID filtern
    existing_bookmark = database_connection.get_bookmark_by_user_and_discussion(g.user.email, discussion_id)

    # Lesezeichen entfernen falls bereits vorhanden, andernfalls hinzufügen
    database_connection.remove_bookmark(g.user.email, discussion_id) if existing_bookmark else database_connection.\
        add_bookmark(g.user.email, discussion_id)

    return redirect(url_for('diskussion_single', diskussion_id=discussion_id))


@app.route('/discussion/<int:discussion_id>/reply/delete/<int:post_id>')
def delete_reply(discussion_id, post_id):
    # Überprüfen ob User angemeldet und ob User Adminrechte besitzt
    if not g.user or not g.user.is_logged_in or not g.user.rechte == "admin":
        return redirect(url_for('login'))

    # Post löschen
    database_connection.delete_reply(post_id)

    return redirect(url_for('diskussion_single', diskussion_id=discussion_id))


@app.route("/add_dataset", methods=["GET", "POST"])
def handle_add_dataset():
    if not g.user or not g.user.is_logged_in:
        return jsonify({"STATUS": 401, "MESSAGE": "Forbidden - You need to be logged in"})

    json_msg = request.json
    dataset_url = json_msg["url"]
    dataset_desc = json_msg["desc"]

    max_file_name_length = 45

    file_name = os.path.basename(dataset_url)[:max_file_name_length]
    path = "./datasets/"
    full_file_name = path + file_name

    result = download_file(dataset_url, full_file_name)

    logger.log("INSERTING", "STARTED TO INSERT")
    csv_action = CSVReader(path, file_name)
    csv_action.insert_into_database(database_connection)
    logger.log("INSERTING DONE", "THE INSERTION HAS FINISHED")

    return jsonify(result)


def download_file(url, file_name):
    try:
        urllib.request.urlretrieve(url, file_name)
        return ["STATUS", 202, "Accepted"]
    except Exception as e:
        return ["STATUS", 500, e]




@app.route("/dataset_export")
def handle_dataset_export():
    if not g.user or not g.user.is_logged_in:
        return redirect(url_for('login'))

    filename = request.args.get("filename")
# If the file in DB
    if filename in database_connection.get_tables()[0]:
        # Retrieve the data
        dataset = [filename, database_connection.get_dataset(filename)]

    else:
        # If the result was not found
        dataset = ["The data you are looking for could not be found",
                   [["please", "try", "again,", "or", "come", "back", "later"]]]


    return render_template("dataset_export.html", filename=filename, dataset=dataset,
                           export_date=datetime.now().strftime("%d.%m.%Y"), row1=request.args.get("row1"),
                           row2=request.args.get("row2"))



def load_users():
    database_connection.exec("DELETE FROM freundesichtbarkeit;")
    # Iterate over the result given by the executed command (Iterate over user list)
    for user in database_connection.exec("SELECT * FROM `user_data`;"):
        firstname = user[0]
        lastname = user[1]
        dob = user[2]
        email = user[3]
        passwort = user[4]
        auth_code = user[5]
        rechte = user[6]
        profil_pic = user[7]
        fav_data = user[8]

        # user_chat_json_data[email] = { "chat_id": "None", "current_chat": "None" }
        chat_data_manager.create_user(email)

        try:
            database_connection.set_freundesichtbarkeit(email, "public")
            profile_visibility_manager.set_profile_visibility(email, "public")
            database_connection.set_profilsichtbarkeit(email, profile_visibility_manager.get_profile_visibility(email))
            user.added_diagrams = user_added_diagrams.get_diagrams(email)
        except:
            pass

        # Append User object to user list
        USERS.append(User(firstname, lastname, dob, email, passwort, auth_code, rechte, profil_pic, fav_data, False))


def start():
    load_users()
    dataset_loader_thread = threading.Thread(target=load_dataset)
    dataset_loader_thread.start()
    socketio.run(app, HOST, PORT, debug=True, allow_unsafe_werkzeug=True)


#
# Misc
#
@app.route('/logs')
def logs():
    return render_template("logs.html", log=logger.get_log())


@app.route("/tests")
def handle_tests():
    return "None"


@app.route("/agb")
def show_agb():
    return render_template("agb.html")


if __name__ == "__main__":
    start()
