from modelFetch import Model
from Infrastructure.hard_guess import HardGuess
import MySQLdb
from Infrastructure.generator import Generator


class User(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def get_by_username(username, connection):
        query = 'SELECT user FROM mysql.user WHERE user = "' + username + '"'
        user = Model.select_db(query, connection)
        return user

    @staticmethod
    def login(username, password):
        # Check whether a user's username and password make a connection to the server
        connection = Model(username, password)
        if connection.connect:
            return True
        return False

    @staticmethod
    def register_credential(connection, data):
        username = data['credentials'][0]['username']
        password = data['credentials'][0]['password']
        user = User.get_by_username(username, connection)
        if user is None:
            is_password_valid = HardGuess.check_password(password)
            if is_password_valid:
                # User doesn't exist, so we can create it
                is_user_registered = User.save(data, connection)
                return is_user_registered
        # User exists
        return False

    @staticmethod
    def save(data, conn):
        username = data['credentials'][0]['username']
        password = data['credentials'][0]['password']
        employee_id = data['credentials'][0]['employee_id']
        hashed_pass = HardGuess.secure_data(password)
        query_create_user = 'CREATE USER "'+username+'"@"LOCALHOST" IDENTIFIED BY "'+hashed_pass+'"'
        is_user_registered = Model.save_user(query_create_user, conn)
        if is_user_registered:
            query_update = 'UPDATE petrol_stations_db.employees SET user = "'+username +'"where employee_id =' +str(employee_id)
            if Model.update(query_update, conn):
                Model.commit(conn)
            else:
                Model.rollback(conn)
                drop_user = 'DROP USER ' + username + '"@"LOCALHOST"'
                Model.drop_user(drop_user, conn)
                return False
        return is_user_registered

    @staticmethod
    def logout(username):
        pass


