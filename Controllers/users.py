import webapp2
from Infrastructure.read_json import ExtractData
from Infrastructure.config import webapp2_config
from Models.user import User


class UserPrivilegeHandler(webapp2.RequestHandler):

    def get(self):
        pass

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        data = self.request.body
        privileges = ExtractData.load_json(data)
        is_granted = User.grant_prev()
        pass


app = webapp2.WSGIApplication([
    ('/user/privileges', UserPrivilegeHandler)
], config=webapp2_config, debug=True)

