import webapp2
from Infrastructure.read_json import ExtractData
from Infrastructure.session import BaseHandler
from Infrastructure.hard_guess import HardGuess
from Models.user import User
from Infrastructure.session import user_required
from Infrastructure.config import webapp2_config
import json


class LoginHandler(BaseHandler):
    def get(self):
        self.render_template('pages/login.html')

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        credentials = dict(self.request.POST)
        username = credentials['username']
        password = credentials['password']
        is_password_valid = HardGuess.check_password(password)
        response_obj = ExtractData.login_response(False)
        if is_password_valid:
            password = HardGuess.secure_data(password)
            connection = User.login(username, password)
            if connection is not None:
                user_ids = User.get_user(username, connection)
                employee = user_ids['employee_id']
                company = user_ids['company_id']
                employee_names = user_ids['first_name'] + ' ' + user_ids['last_name']
                email = user_ids['email']
                urls = User.get_urls(employee, connection)
                user = {'user': username, 'pass': password, 'employee_id': employee, 'company_id': company, 'urls': urls, 'email': email}
                self.session['user_id'] = user
                response_obj = ExtractData.login_response(True, employee_names)
        self.response.write(json.dumps(response_obj))


class HomeHandler(BaseHandler):
    @user_required
    def get(self):
        urls = {
            'registration/company': 'Company Registration',
            'registration/employee': 'Employee Registration',
            'registration/client': 'Client Registration',
            'registration/user': 'Create User',
            'company/actions': 'Actions On Company'
        }
        context = {
            'urls': urls
        }
        self.render_template('pages/home.html', **context)

    @user_required
    def post(self):
        pass


class LogoutHandler(BaseHandler):
    @user_required
    def get(self):
        self.session.clear()
        # User is logged out, let's try redirecting to login page
        try:
            self.redirect('/login')
        except (AttributeError, KeyError), e:
            self.response.write("User is logged out")


app = webapp2.WSGIApplication([
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/home', HomeHandler)
], config=webapp2_config, debug=True)



