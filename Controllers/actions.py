import webapp2
from Infrastructure.session import BaseHandler
from Infrastructure.session import user_required
from Infrastructure.config import webapp2_config


class CompanyActionsHandler(BaseHandler):
    @user_required
    def get(self):
        self.render_template('pages/company_actions.html')

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        pass


app = webapp2.WSGIApplication([
    ('/company/actions', CompanyActionsHandler)
], config=webapp2_config, debug=True)



