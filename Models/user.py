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
    def get_user(username, connection):
        query = 'SELECT E.employee_id, first_name, last_name, T.company_id, A.email FROM employees E JOIN titles T ON E.title_id = T.title_id JOIN addresses A ON A.address_id = E.address_id WHERE E.user = "'+username+'"'
        user = Model.select_db(query, connection)
        return user

    @staticmethod
    def login(username, password):
        # Check whether a user's username and password make a connection to the server
        connection = Model(username, password)
        return connection.connect

    @staticmethod
    def register_credential(data, connection):
        username = data['credentials']['username']
        password = data['credentials']['password']
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
        username = data['credentials']['username']
        password = data['credentials']['password']
        employee_id = data['credentials']['employee_id']
        hashed_pass = HardGuess.secure_data(password)
        query_create_user = 'CREATE USER "'+username+'"@"LOCALHOST" IDENTIFIED BY "'+hashed_pass+'"'
        is_user_registered = Model.execute_query(query_create_user, conn)
        if is_user_registered:
            query_update = 'UPDATE employees SET user = "'+username + '"where employee_id =' +str(employee_id)
            if Model.execute_query(query_update, conn):
                Model.commit(conn)
            else:
                Model.rollback(conn)
                drop_user = 'DROP USER ' + username + '"@"LOCALHOST"'
                Model.execute_query(drop_user, conn)
                return False
        return is_user_registered

    @staticmethod
    def get_urls(employee_id, connection):
        query = 'SELECT urls.url_name from urls INNER JOIN urls_for_employees ON urls.url_id = urls_for_employees.url_id WHERE urls_for_employees.employee_id = {0}'.format(employee_id)
        urls = Model.select_db_many(query, connection)
        urls = [item['url_name'] for item in urls]
        return urls

    @staticmethod
    def grant_prev(privileges, connection):
        pass
