import webapp2
import MySQLdb
from Models.registry import Registry
from Models.user import User
from Infrastructure.read_json import ExtractData
from Infrastructure.session import user_required
from Infrastructure.session import BaseHandler
from Infrastructure.config import webapp2_config
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


class RegisterCompanyActivity(BaseHandler):
    @user_required
    def get(self):
        pass

    @user_required
    def post(self):
        self.response.headers['Content-type'] = 'application/json'
        data = self.request.body
        activity = ExtractData.load_json(data)
        conn = self.get_connection()
        is_registered = Registry.register_company_activity(activity, conn)
        pass


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
        is_registered = User.register_credential(user, conn)
        self.response.write(is_registered)
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))
        self.response.write(is_registered)
        conn.close()
        pass


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


app = webapp2.WSGIApplication([
    ('/register/company', RegisterCompanyHandler),
    ('/register/title', RegisterCompanyPostTitle),
    ('/register/activity', RegisterEmployeeHandler),
    ('/register/employee', RegisterEmployeeHandler),
    ('/register/user', RegisterUserHandler),
    ('/register/client', RegisterClientHandler)
], config=webapp2_config, debug=True)



