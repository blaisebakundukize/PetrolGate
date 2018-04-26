import webapp2
import MySQLdb
from Models.registry import Registry
from Models.user import User
from Infrastructure.read_json import ExtractData
from Infrastructure.session import user_required
from Infrastructure.session import BaseHandler
import json


class RegisterCompanyHandler(BaseHandler):
    @user_required
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('its working here')

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        data = self.request.body
        company = ExtractData.load_json(data)
        conn = self.get_connection()
        if conn:
            is_registered = Registry.register_company(company, conn)
            response_obj = ExtractData.response(is_registered)
            self.response.write(json.dumps(response_obj))
        conn.close()


class RegisterEmployeeHandler(BaseHandler):
    @user_required
    def get(self):
        pass

    @user_required
    def post(self):
        self.response.headers['Content-type'] = 'application/json'
        data = self.request.body
        employee = ExtractData.load_json(data)
        conn = self.get_connection()
        is_registered = Registry.register_employee(employee, conn)
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))
        # self.response.write(is_registered)
        conn.close()


class RegisterUserHandler(BaseHandler):
    @user_required
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        pass

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        data = self.request.body
        user = ExtractData.load_json(data)
        conn = self.get_connection()
        is_registered = User.register_credential(conn, user)
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))
        self.response.write(is_registered)
        conn.close()
        pass


class RegisterCompanyPostTitle(BaseHandler):
    @user_required
    def get(self):
        pass

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        data = self.request.body
        titles = ExtractData.load_json(data)
        conn = self.get_connection()
        is_registered = Registry.register_company_post_title(titles, conn)
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))
        conn.close()


class RegisterClientHandler(BaseHandler):
    @user_required
    def get(self):
        pass

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        data = self.request.body
        client = ExtractData.load_json(data)
        conn = self.get_connection()
        is_registered = Registry.register_client(client, conn)
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))
        # self.response.write(is_registered)
        conn.close()


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '51336f49-063e-4d2b-ba06-6e0410113c64',
}

app = webapp2.WSGIApplication([
    ('/register/company', RegisterCompanyHandler),
    ('/register/user', RegisterUserHandler),
    ('/register/employee', RegisterEmployeeHandler),
    ('/register/title', RegisterCompanyPostTitle),
    ('/register/client', RegisterClientHandler)
], config=config, debug=True)



