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
        is_registered = Registry.register_company(company, conn)
        conn.close()
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))


class RegisterCompanyPostTitle(BaseHandler):
    @user_required
    def get(self):
        pass

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        titles = dict(self.request.POST)
        conn = self.get_connection()
        company_id = self.get_user_company_id()
        is_registered = Registry.register_company_post_title(company_id, titles, conn)
        conn.close()
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))


class RegisterCompanyActivity(BaseHandler):
    @user_required
    def get(self):
        pass

    @user_required
    def post(self):
        self.response.headers['Content-type'] = 'application/json'
        activities = dict(self.request.POST)
        conn = self.get_connection()
        company_id = self.get_user_company_id()
        is_registered = Registry.register_company_activity(company_id, activities, conn)
        conn.close()
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))


class RegisterCompanyStation(BaseHandler):
    @user_required
    def get(self):
        data = self.request.body
        self.response.write(data)

    # @user_required
    def post(self):
        self.response.headers['Content-type'] = 'application/json'
        data = self.request.body
        stations = ExtractData.load_json(data)
        self.response.write(type(stations['stations']))
        conn = self.get_connection()
        company_id = self.get_user_company_id()
        is_registered = Registry.register_station(company_id, stations, conn)
        self.response.write(is_registered)
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
        conn.close()
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))


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
        conn.close()
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))


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
        conn.close()
        response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(response_obj))


app = webapp2.WSGIApplication([
    ('/register/company', RegisterCompanyHandler),
    ('/register/title', RegisterCompanyPostTitle),
    ('/register/activity', RegisterCompanyActivity),
    ('/register/station', RegisterCompanyStation),
    ('/register/employee', RegisterEmployeeHandler),
    ('/register/user', RegisterUserHandler),
    ('/register/client', RegisterClientHandler)
], config=webapp2_config, debug=True)



