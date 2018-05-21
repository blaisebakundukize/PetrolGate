import webapp2
from Infrastructure.session import BaseHandler
from Infrastructure.config import webapp2_config
from Models.payment_options import PaymentOptions
from Infrastructure.session import user_required
from Infrastructure.read_json import ExtractData
from Infrastructure.generator import Generator
import json


class CardStockHandler(BaseHandler):
    @user_required
    def get(self):
      pass

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        data = dict(self.request.POST)
        number_of_cards = int(data['number'])
        conn = self.get_connection()
        company_id = self.get_user_company_id()
        # cards_content = Generator.card_content(number_of_cards, company_id)
        is_contents_saved = PaymentOptions.save_card_content(number_of_cards, company_id, conn)
        conn.close()
        # response_obj = ExtractData.response(is_contents_saved)
        # self.response.write(json.dumps(response_obj))
        self.response.write(is_contents_saved)


class AssignCardHandler(BaseHandler):
    @user_required
    def get(self):
      pass

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        data = dict(self.request.POST)
        conn = self.get_connection()
        if "assign_card_number" in data:
            is_card_assigned = PaymentOptions.assign_card(data, conn)
            conn.close()
            self.response.write(is_card_assigned)
            response_obj = ExtractData.response(is_card_assigned)
            self.response.write(json.dumps(response_obj))


class BookletsStockHandler(BaseHandler):
    @user_required
    def get(self):
      pass

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        pass


app = webapp2.WSGIApplication([
    ('/stock/cards', CardStockHandler),
    ('/stock/booklets', BookletsStockHandler),
    ('/stock/assign/card', AssignCardHandler)
], config=webapp2_config, debug=True)



