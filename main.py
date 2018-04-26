from Models.modelFetch import Model
import webapp2

conn = Model('root','Blaise32')


class MainPage(webapp2.RequestHandler):

    def get(self):
        """Simple request handler that shows all of the MySQL variables."""
        self.response.headers['Content-Type'] = 'text/plain'
        self.conn = conn.connect
        cursor = self.conn.cursor()
        cursor.execute('SHOW DATABASES')

        for r in cursor.fetchall():
            self.response.write('{}\n'.format(r))
        conn.close


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)