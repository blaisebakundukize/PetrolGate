from Models.modelFetch import Model
from Infrastructure.hard_guess import HardGuess
from Infrastructure.generator import Generator


class PaymentOptions(object):

    def __init__(self):
        pass

    @staticmethod
    def save_card_content(number_of_cards, company_id, connection):
        card_ids = Generator.generate_identity(number_of_cards)
        credential_ids = Generator.generate_identity(number_of_cards)
        values = PaymentOptions.card_content(card_ids, credential_ids, company_id)
        query_insert_credentials = 'INSERT INTO card_credentials (credential_id) VALUES ' + values['values_cred']
        query_insert_cards = 'INSERT INTO stock_cards (card_number, company_id, credential_id) VALUES '+ values['values_card']
        is_credentials_saved = Model.execute_query(query_insert_credentials, connection)
        is_card_content_saved = Model.execute_query(query_insert_cards, connection)
        if is_credentials_saved and is_card_content_saved:
            Model.commit(connection)
            return True
        else:
            Model.rollback(connection)
        return False

    @staticmethod
    def assign_card(data, connection):
        card_number = data['assign_card_number']
        account_id = data['account_id']
        password = data['password']
        confirm_password = data['confirm_password']
        # validate password
        is_passed = HardGuess.validate_password(password, confirm_password)
        if is_passed is False:
            return False
        password_hashed = HardGuess.secure_data(password)
        query_select_credential_id = 'SELECT BIN_TO_UUID(credential_id) credential_id FROM stock_cards WHERE card_number = UNHEX("{0}")'.format(card_number)
        credential = Model.select_db(query_select_credential_id, connection)
        if credential is None:
            return False
        credential_id = credential['credential_id']
        query_insert_card_assigned = 'INSERT INTO cards (card_number, account_id, credential_id) VALUES (UUID_HEX_TO_BIN("{0}"),{1},UUID_HEX_TO_BIN("{2}"))'.format(card_number, account_id, credential_id)
        query_update_credential_password = 'UPDATE card_credentials SET password = UNHEX("{0}") WHERE credential_id = UNHEX("{1}")'.format(password_hashed, credential_id)
        # execute queries
        is_card_assigned = Model.execute_query(query_insert_card_assigned, connection)
        is_credential_updated= Model.execute_query(query_update_credential_password, connection)
        # check executed queries
        if is_card_assigned and is_credential_updated:
            Model.commit(connection)
            return True
        else:
            Model.rollback(connection)
            return False

    @staticmethod
    def card_content(card_ids, credential_ids, company_id):
        """ process values to pass into insert query for cards-contents insertion
        :param card_ids: list of card ids
        :param credential_ids: list of credential ids
        :param company_id: identify company by capturing it's id from database
        :return: return values as string
        """
        count = 0
        length = len(card_ids)
        values_cards = ''
        values_creds = ''
        for (a, b) in zip(card_ids, credential_ids):
            count += 1
            values_cards += '(' + a + ', ' + str(company_id) + ', ' + b + ')'
            values_creds += '('+b+')'
            if count != length:
                values_cards += ', '
                values_creds += ', '
        values = {'values_card': values_cards, 'values_cred': values_creds}
        return values

