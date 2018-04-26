import webapp2
from Models.user import User
from Infrastructure.read_json import ExtractData
from Models.modelFetch import Model

connection = Model('root', 'Blaise32')


class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        conn = connection.connect
        cursor = conn.cursor()
        cursor.execute('SHOW DATABASES')
        self.response.write("good")
        for r in cursor.fetchall():
            self.response.write('{}\n'.format(r))
        connection.close

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        # data = self.request.body
        # info = ExtractData.load_json(data)
        # user_id = 1
        connection = Model('root', 'Blaise32')
        if connection:
            address_id = 'SELECT MAX(address_id + 1) FROM ADDRESSES'
            cursor = connection.cursor()
            cursor.execute('SHOW DATABASES')
            if cursor:
                self.response.write("done")
            for r in cursor.fetchall():
                self.response.write(r)


app = webapp2.WSGIApplication([
    ('/company', RegisterHandler)])



