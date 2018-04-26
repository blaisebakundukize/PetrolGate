import webapp2
from Infrastructure.read_json import ExtractData
from Infrastructure.session import BaseHandler
from Infrastructure.hard_guess import HardGuess
from Models.user import User
from Infrastructure.session import user_required


class LoginHandler(BaseHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.get_user())
        # self.response.write(conn)

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        credentials = self.request.body
        user = ExtractData.load_json(credentials)
        username = user['credentials'][0]['username']
        password = user['credentials'][0]['password']
        is_password_valid = HardGuess.check_password(password)
        if is_password_valid:
            password = HardGuess.secure_data(password)
            is_logged = User.login(username, password)
            if is_logged:
                user = {'user': username, 'pass': password}
                self.session['user_id'] = user
                self.response.write('session is set')
        else:
            # password should contains at least one capital letter, one digit, and not less than 8 characters
            self.response.write('password is not valid')
            pass


class LogoutHandler(BaseHandler):
    @user_required
    def get(self):
        self.session.clear()
        self.response.write('User logged out')


key = '51336f49-063e-4d2b-ba06-6e0410113c64'
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': key,
    # 'backends': {'securecookie': 'webapp2_extras.sessions.SecureCookieSessionFactory'}
}

app = webapp2.WSGIApplication([
    ('/login', LoginHandler),
    ('/logout', LogoutHandler)
], config=config, debug=True)



