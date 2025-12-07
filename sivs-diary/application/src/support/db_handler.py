import logging
import os
from dotenv import load_dotenv, find_dotenv
import psycopg2
from flask import jsonify
from dotenv import load_dotenv
load_dotenv(find_dotenv())
class DBHandler():
    """
    Die DBHandler Klasse ist das Herz der Anwendung, diese kommuniziert mit der Datenbank und interpretiert Parameter.
    Auch generiert diese Response Code und gibt diese an die Blueprints zurück
    """

    def __init__(self,
                 user=os.environ.get("POSTGRES_USER"),
                 password=os.environ.get("POSTGRES_PASSWORD"),
                 host="localhost",  # When running locally or outside Docker network
                 port="5432",
                 dbname=os.environ.get("POSTGRES_DB")):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        """
        Datenbank Connect wird durchgeführt
        :return:
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
        except Exception as ex:
            logging.error(ex)


    def disconnect(self):
        self.connection.close()

    def execute_query(self,query, values=(),fetchone=False,fetch=True):
        """
        Fügt ein Datenbankquery durch.
        :param query: Query "SELECT STATEMENT"
        :param values: Query-Parameter falls paramaterized Queries verwendet werden
        :param fetchone: Gibt es eine oder mehrere Rückgabewerte
        :param fetch: Gibt es einen Rückgabewer
        :return:
        """
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            if fetchone is True and fetch is True:
                result = self.cursor.fetchone()
                return result
            if fetchone is False and fetch is True:
                result = self.cursor.fetchall()
                column_names = [desc[0] for desc in self.cursor.description]
                data = [dict(zip(column_names, row)) for row in result]
                return data
            if fetch is False:
                return True
        except Exception as ex:
            logging.error(ex)
            self.connection.rollback()
            return None

    def checkPassword(self,username,password):
        """
        Prüft ob ein Passwort mit dem Passwort in der Datenbank übereinstimmt.
        :param username:
        :param password:
        :return:
        """
        user_query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        result = self.execute_query(user_query, (username, password), fetchone=True)
        if result:
            return jsonify({
                'message': 'Logged In',
                'homelink': f'/pages/diary.html?username={username}'
            })
        else:
            return jsonify({
                'message': 'Error logging in!'
            }), 401
    def getUserId(self, username):
        """
        Holt die UserID eines usernamen,
        :param username:
        :return:
        """
        user_id_query = "SELECT id FROM Users WHERE username = %s"
        user_id = self.execute_query(user_id_query, (username,), fetchone=True)
        if user_id:
            user_id = user_id[0]
        return user_id

    def createDiaryEntry(self, username, entry):
        """
        Erstellt einen Tagebucheintrag in der Datenbank
        :param username:
        :param entry:
        :return:
        """
        user_id = self.getUserId(username=username)
        title = entry["entry_title"]
        content = entry["entry_content"]
        date = entry["entry_date"]
        if user_id:
            insert_query = "INSERT INTO DiaryEntries (user_id,entry_title,entry_content,entry_date) VALUES (%s, %s, %s, %s)"
            self.execute_query(insert_query, (user_id, title, content, date), fetch=False)
            return jsonify({'message': 'Diary Entry created!'})
        else:
            return jsonify({'message': 'Error!'})

    def deleteDiary(self,id):
        """
        Löscht einen Tagebucheintrag
        :param id:
        :return:
        """
        delete_query = "DELETE FROM DiaryEntries WHERE id=%s"
        result = self.execute_query(delete_query, (id,), fetch=False)
        if result:
            return jsonify({'message': 'Diary Entry deleted!'})
        else:
            return jsonify({'message': 'Error deleting Diary Entry!'})

    def getDiary(self, username, searchparameter):
        """
        Lädt die Tagebucheinträge eines Users aus der Datenbank
        :param username:
        :return:
        """
        user_id = self.getUserId(username=username)
        print(f"Querying {username} for diary entries filter {searchparameter}")
        if not searchparameter or searchparameter == "null":
            searchparameter = ""
        if user_id:
            entries_query = """
                    SELECT id, entry_title, entry_content, entry_date 
                    FROM DiaryEntries d 
                    WHERE d.user_id = %s 
                      AND (LOWER(d.entry_content) LIKE %s OR LOWER(d.entry_title) LIKE %s) 
                    ORDER BY entry_date desc
                """
            search_pattern = f"%{searchparameter}%"
            print(entries_query)
            entries = self.execute_query(entries_query, (user_id, search_pattern, search_pattern))
            print(entries)
            if entries is not None:
                return jsonify(entries)
            else:
                return []
        else:
            return jsonify({'message': 'User not found'}),400

    def resetPassword(self, username,password,secret_answer):
        """
        Setzt das Password bei richtiger Geheimantwort zurück
        :param username:
        :return:
        """
        # Datenbank Query sucht den User und prüft ob die Geheimantwort übereinstimmt
        user_id_query = "SELECT id FROM Users WHERE username = %s and secret_answer = %s"
        user_id = self.execute_query(user_id_query, (username, secret_answer), fetchone=True)
        if user_id:
            pw_update_query = "UPDATE Users SET password = %s WHERE id=%s"
            result = self.execute_query(pw_update_query, (password, user_id[0]), fetch=False)
            return jsonify({'message': 'Password reset successful!'})
        else:
            return jsonify({'message': 'Wrong answer!'})

        def insertUser(self, username,password,secret_question,secret_answer):
            """
            Erstellt einen neuen Benutzer in der Datenbank
            :param username:
            :param password:
            :param secret_question:
            :param secret_answer:
            :return:
            """
            user_id = self.getUserId(username)
            #Prüfen ob der Username eventuell schon existiert, falls ja Fehlermeldung
            if user_id:
                return jsonify({'message': 'User already existing'}),400
            # Datenbank Query für das Erstellen eines Benutzers
            insert_user_query = "INSERT INTO Users (username, password, secret_question, secret_answer) VALUES (%s, %s, %s, %s)"
            user = self.execute_query(insert_user_query, (username, password, secret_question, secret_answer), fetch=False)
            # Wenn der User erfolgreich erstellt wurde Erfolgsmeldung, ansonsten Fehlermeldung
            if user:
                return jsonify({'message': 'User created'}),200
            else:
                return jsonify({'message': 'Usercreation failed'}),400

    def getSecretQuestion(self, username):
        """
        Es wird die Geheimfrage eines Benutzers abgefragt. Diese wird benötigt um einen Passwort-Reset durchzuführen.
        Aktuell nicht im Frontend enthalten
        :param username:
        :return:
        """
        user_id = self.getUserId(username)
        if user_id:
            #Datenbank Query für das Abfragen der Geheimfrage
            secret_question_query = "SELECT secret_question FROM Users WHERE id=%s"
            secret_question = self.execute_query(secret_question_query, (user_id,), fetchone=True)
            #Falls Frage vorhanden wird diese als JSON zurückgemeldet, anderenfalls eine Fehlermeldung
            if secret_question:
                return jsonify({'secret_question': f'{secret_question[0]}'})