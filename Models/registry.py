from Models.modelFetch import Model
from Infrastructure.generator import Generator


class Registry(object):

    def __init__(self):
        pass

    @staticmethod
    def register_query(values, table):
        cols = '('
        v = 'VALUES ('
        length = len(values)
        for index, (key, value) in enumerate(values.items()):
            cols += key + ''
            v += '"' + str(value) + '"'
            if index != length - 1:
                cols += ','
                v += ','
        query = 'INSERT INTO ' + table + cols + ')' + v + ')'
        return query

    @staticmethod
    def next_id(connection, table, column):
        select_next_address_id = 'SELECT IFNULL(MAX(' + column + ' + 1),1) AS address_id FROM ' + table
        next_address_id = Model.select_db(select_next_address_id, connection)
        return next_address_id['address_id']

    @staticmethod
    def register(table, address, identity, connection):
        addresses_table = 'petrol_stations_db.addresses'
        query_address = Registry.register_query(address, addresses_table)
        column_address_id = 'address_id'
        next_address_id = Registry.next_id(connection, addresses_table, column_address_id)
        if next_address_id:
            identity['address_id'] = next_address_id
            query_identity = Registry.register_query(identity, table)
            # return query_identity
            if Model.execute_query(query_address, connection) and Model.execute_query(query_identity, connection):
                Model.commit(connection)
                return True
            else:
                Model.rollback(connection)
                return False
        else:
            return False

    @staticmethod
    def register_company(data, connection):
        table = 'petrol_stations_db.petrol_station_companies'
        company = data['company'][0]
        address = data['address'][0]
        is_registered = Registry.register(table, address, company, connection)
        return is_registered

    @staticmethod
    def register_employee(data, connection):
        table = 'petrol_stations_db.employees'
        address = data['address'][0]
        employee = data['employee'][0]
        is_registered = Registry.register(table, address, employee, connection)
        return is_registered

    @staticmethod
    def register_client(data, connection):
        table_client = 'petrol_stations_db.clients'
        table_addresses = 'petrol_stations_db.addresses'
        table_account_identifier = 'petrol_stations_db.account_identifier'
        table_account = 'petrol_stations_db.accounts'
        account_number_column = 'account_number'
        column_address_id = 'address_id'
        column_client_id = 'client_id'
        next_account_identifier = Registry.next_id(connection, table_account_identifier, account_number_column)
        next_address_id = Registry.next_id(connection, table_addresses, column_address_id)
        next_client_id = Registry.next_id(connection, table_client, column_client_id)
        address = data['address'][0]
        client = data['client'][0]
        account = data['account'][0]
        company = client['company_id']

        account_number = Generator.generate_account(company, next_account_identifier)

        client['address_id'] = next_address_id
        account['account_number'] = account_number
        account['client_id'] = next_client_id

        is_registered = Registry.new_account_number(connection, client, address, account,
                                                    table_client, table_addresses, table_account)
        return is_registered

    @staticmethod
    def new_account_number(connection, client, address, account, table_client, table_addresses, table_account):
        query_client = Registry.register_query(client, table_client)
        query_address = Registry.register_query(address, table_addresses)
        query_account = Registry.register_query(account, table_account)
        query_account_identifier = 'INSERT INTO petrol_stations_db.account_identifier values()'
        insert_address = Model.execute_query(query_address, connection)
        insert_client = Model.execute_query(query_client, connection)
        insert_account = Model.execute_query(query_account, connection)
        insert_account_identifier = Model.execute_query(query_account_identifier, connection)
        if insert_address and insert_client and insert_account and insert_account_identifier:
            Model.commit(connection)
            return True
        else:
            Model.rollback(connection)
            return False

    @staticmethod
    def register_mutliple_title_query(company_id, data, table):
        cols = '('
        v = 'VALUES '
        query = 'INSERT INTO ' + table + '(title_name, company_id)'
        length = len(data)
        for index, title in enumerate(data):
            v += '("' + str(title) + '",' + '"' + str(company_id) + '")'
            if index != length - 1:
                v += ','
        query += v
        return query

    @staticmethod
    def register_company_post_title(data, connection):
        company_id = data['company'][0]['company_id']
        titles = data['title_name']
        table = 'petrol_stations_db.titles'
        query = Registry.register_mutliple_title_query(company_id, titles, table)
        is_titles_registerd = Model.execute_query(query, connection)
        if is_titles_registerd:
            Model.commit(connection)
            return True
        else:
            return False

    @staticmethod
    def register_company_activity(activity, connection):
        pass
