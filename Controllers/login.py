import webapp2
import jinja2
import os
from Infrastructure.read_json import ExtractData
from Infrastructure.session import BaseHandler
from Infrastructure.hard_guess import HardGuess
from Models.user import User
from Infrastructure.session import user_required
from Infrastructure.config import webapp2_config


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '../templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class LoginHandler(BaseHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        # template = JINJA_ENVIRONMENT.get_template('modal.html')
        # self.response.write(template.render())
        self.response.write(self.get_user())
        # self.response.write()
        self.response.write("connection established")

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        credentials = dict(self.request.POST)
        username = credentials['username']
        password = credentials['password']
        is_password_valid = HardGuess.check_password(password)
        if is_password_valid:
            password = HardGuess.secure_data(password)
            connection = User.login(username, password)
            if connection is not None:
                ids = User.get_ids(username, connection)
                employee = ids['employee_id']
                company = ids['company_id']
                user = {'user': username, 'pass': password, 'employee_id': employee, 'company_id': company}
                self.session['user_id'] = user
                self.response.write('session is set')
            else:
                # username or password not valid
                self.response.write('Username or password is not valid')
        else:
            # password should contains at least one capital letter, one digit, and not less than 8 characters
            self.response.write('password is not valid')
            pass


class LogoutHandler(BaseHandler):
    @user_required
    def get(self):
        self.session.clear()
        self.response.write('User logged out')


app = webapp2.WSGIApplication([
    ('/login', LoginHandler),
    ('/logout', LogoutHandler)
], config=webapp2_config, debug=True)



