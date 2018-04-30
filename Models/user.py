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
    def get_ids(username, connection):
        employee = 'petrol_stations_db.employees'
        title = 'petrol_stations_db.titles'
        query = 'SELECT '+employee+ '.employee_id, ' + title + '.company_id from '+employee+' INNER JOIN '+title+ ' ON ' +employee+ '.title_id = ' +title+ '.title_id WHERE '+employee+ '.user = "'+username+'"'
        ids = Model.select_db(query, connection)
        return ids

    @staticmethod
    def login(username, password):
        # Check whether a user's username and password make a connection to the server
        connection = Model(username, password)
        return connection.connect

    @staticmethod
    def register_credential(data, connection):
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
        is_user_registered = Model.execute_query(query_create_user, conn)
        if is_user_registered:
            query_update = 'UPDATE petrol_stations_db.employees SET user = "'+username +'"where employee_id =' +str(employee_id)
            if Model.execute_query(query_update, conn):
                Model.commit(conn)
            else:
                Model.rollback(conn)
                drop_user = 'DROP USER ' + username + '"@"LOCALHOST"'
                Model.execute_query(drop_user, conn)
                return False
        return is_user_registered

    @staticmethod
    def grant_prev(privileges, connection):
        pass
