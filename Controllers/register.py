import webapp2
from Models.registry import Registry
from Models.user import User
from Infrastructure.read_json import ExtractData
from Infrastructure.session import user_required
from Infrastructure.session import BaseHandler
from Infrastructure.config import webapp2_config
from Models.modelFetch import Model
import json


class RegisterCompanyHandler(BaseHandler):
    @user_required
    def get(self):
        self.render_template('pages/registration.html')

    @user_required
    def post(self):
        data = self.request.body
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        company = json.loads(data)
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
        self.response.headers['Access-Control-Allow-Origin'] = '*'
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
        self.response.headers['Access-Control-Allow-Origin'] = '*'
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
        pass

    @user_required
    def post(self):
        self.response.headers['Content-type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        data = self.request.body
        stations = ExtractData.load_json(data)
        conn = self.get_connection()
        company_id = self.get_user_company_id()
        is_registered = Registry.register_station(company_id, stations, conn)
        conn.close()
        response_obj = ExtractData.response(is_registered)
        self.response.write(response_obj)


class RegisterEmployeeHandler(BaseHandler):
    @user_required
    def get(self):
        self.render_template('pages/employee-registration.html')

    @user_required
    def post(self):
        self.response.headers['Content-type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
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
        self.render_template('pages/user-credentials.html')

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
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
        self.render_template('pages/client_registration.html')

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        data = self.request.body
        client = ExtractData.load_json(data)
        conn = self.get_connection()
        company_id = self.get_user_company_id()
        is_registered = Registry.register_client(company_id, client, conn)
        conn.close()
        # response_obj = ExtractData.response(is_registered)
        self.response.write(json.dumps(is_registered))


app = webapp2.WSGIApplication([
    ('/registration/company', RegisterCompanyHandler),
    ('/registration/title', RegisterCompanyPostTitle),
    ('/registration/activity', RegisterCompanyActivity),
    ('/registration/station', RegisterCompanyStation),
    ('/registration/employee', RegisterEmployeeHandler),
    ('/registration/user', RegisterUserHandler),
    ('/registration/client', RegisterClientHandler)
], config=webapp2_config, debug=True)



