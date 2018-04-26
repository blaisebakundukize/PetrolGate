import MySQLdb


class Model(object):

    host = 'localhost'
    connection = None

    def __init__(self, user, password):
        self.user = user
        self.password = password

    @property
    def connect(self):
        try:
            self.connection = MySQLdb.connect(self.host, self.user, self.password)
            return self.connection
        except MySQLdb.Error as error:
            print(error)
            return self.connection

    @staticmethod
    def close(connection):
        connection.close()
        print("Connection Closed")

    @staticmethod
    def commit(connection):
        connection.commit()

    @staticmethod
    def rollback(connection):
        connection.rollback()

    @staticmethod
    def insert(query, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            return True
        except MySQLdb.Error, e:
            print(e)
            return False

    @staticmethod
    def select_address_id(query, connection):
        if connection:
            cursor = connection.cursor()
            try:
                address_id = None
                cursor.execute(query)
                for idd in [int(r[0]) for r in cursor.fetchall()]:
                    address_id = idd  # type: int
                return address_id
            except MySQLdb.Error, e:
                print e
                return None

    @staticmethod
    def select_db(query, connection):
        if connection:
            cursor = connection.cursor()
            try:
                data = None
                cursor.execute(query)
                result = cursor.fetchall()
                if result:
                    for i in result:
                        data = i
                    return data
                else:
                    return None
            except MySQLdb.Error, e:
                print(e)
                return None

    @staticmethod
    def save_user(query, connection):
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query)
                return True
            except MySQLdb.Error, e:
                print(e)

    @staticmethod
    def update(query, connection):
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query)
                return True
            except MySQLdb.Error, e:
                print(e)
                return False

    @staticmethod
    def drop_user(query, connection):
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query)
                return True
            except MySQLdb.Error, e:
                print(e)
                return False
































