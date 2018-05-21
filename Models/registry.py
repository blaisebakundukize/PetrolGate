from Models.modelFetch import Model
from Infrastructure.generator import Generator
import uuid
import re


class Registry(object):

    def __init__(self):
        pass

    @staticmethod
    def register_query(values, table):
        """ process dictionary data and return an insert query
        :param values: dictionary data
        :param table: name of table
        :return: query processed from the given data
        """
        cols = '('
        v = ' VALUES ('
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
        select_next_id = 'SELECT IFNULL(MAX(' + column + ' + 1),1) AS id FROM ' + table
        next_id = Model.select_db(select_next_id, connection)
        return next_id['id']

    @staticmethod
    def register(table, address, identity, connection):
        addresses_table = 'addresses'
        address_id = 'UUID_TO_BIN("'+str(uuid.uuid1())+'")'
        address['address_id'] = 'ADDRESS(UUID)'
        identity['address_id'] = 'ADDRESS(UUID)'
        query_address = Registry.register_query(address, addresses_table)
        query_identity = Registry.register_query(identity, table)

        # replace 'ADDRESS(UUID)' with a valid uuid
        query_address = query_address.replace('"ADDRESS(UUID)"', address_id)
        query_identity = query_identity.replace('"ADDRESS(UUID)"', address_id)

        if Model.execute_query(query_address, connection) and Model.execute_query(query_identity, connection):
            Model.commit(connection)
            return True
        else:
            Model.rollback(connection)
            return False

    @staticmethod
    def register_company(data, connection):
        table = 'petrol_station_companies'
        company = data['company_identification']
        address = data['company_address']
        is_registered = Registry.register(table, address, company, connection)
        return is_registered

    @staticmethod
    def register_employee(data, connection):
        table = 'employees'
        address = data['address']
        employee = data['employee']
        is_registered = Registry.register(table, address, employee, connection)
        return is_registered

    @staticmethod
    def register_client(company_id, data, connection):
        table_client = 'clients'
        table_addresses = 'addresses'
        table_account_identifier = 'account_identifier'
        table_account = 'accounts'
        account_number_column = 'account_number'

        next_account_identifier = Registry.next_id(connection, table_account_identifier, account_number_column)

        address = data['address']
        client = data['client']
        account = data['account']

        # add company id on client and account details
        client['company_id'] = company_id
        account['company_id'] = company_id

        # genetate account number
        account_number = Generator.generate_account(company_id, next_account_identifier)
        account['account_number'] = account_number

        # add fake UUID keys on client, address, and account details
        client['address_id'] = 'ADDRESS(UUID)'
        client['client_id'] = 'CLIENT(UUID)'
        address['address_id'] = 'ADDRESS(UUID)'
        account['client_id'] = 'CLIENT(UUID)'

        is_registered = Registry.new_account_number(connection, client, address, account,
                                                    table_client, table_addresses, table_account)
        return is_registered

    @staticmethod
    def new_account_number(connection, client, address, account, table_client, table_addresses, table_account):
        """ call functions for forming query, and registering new client into database along with addresses and account
        :param connection: connection to the server
        :param client: client information in type of dict
        :param address: addresses in type of dict
        :param account: account number
        :param table_client: table name of client
        :param table_addresses: table name of addresses
        :param table_account: table name of accounts
        :return: true if query execution is successful, or False conversely
        """

        address_id = 'UUID_TO_BIN("' + str(uuid.uuid1()) + '")'
        client_id = 'UUID_TO_BIN("' + str(uuid.uuid1()) + '")'

        query_address = Registry.register_query(address, table_addresses)
        query_client = Registry.register_query(client, table_client)
        query_account = Registry.register_query(account, table_account)

        # replace 'ADDRESS(UUID)' with a valid uuid
        query_address = query_address.replace('"ADDRESS(UUID)"', address_id)
        query_client = query_client.replace('"ADDRESS(UUID)"', address_id)
        query_client = query_client.replace('"CLIENT(UUID)"', client_id)
        query_account = query_account.replace('"CLIENT(UUID)"', client_id)

        query_account_identifier = 'INSERT INTO account_identifier values()'
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
    def insert_from_list(company_id, data, table, columns):
        """ process data which is a List type, and return query
        :param company_id: company id to where each item from list goes with
        :param data: values in type of List
        :param table: name of table
        :param columns: names of columns
        :return: insert query
        """

        v = ' VALUES '
        query = 'INSERT INTO ' + table + columns
        length = len(data)
        for index, item in enumerate(data):
            v += '("' + str(item) + '",' + '"' + str(company_id) + '")'
            if index != length - 1:
                v += ','
        query += v
        return query

    @staticmethod
    def register_company_post_title(company_id, title, connection):
        """ call functions, one for forming an insert query, and another for executing query
        :param company_id: company Identification in database
        :param title: values in type of List
        :param connection: connection to the server
        :return: true if query execution is successful, or False conversely
        """
        titles = title['title_name'].split(',')
        table = 'titles'
        columns = ' (title_name, company_id)'
        query = Registry.insert_from_list(company_id, titles, table, columns)
        is_titles_registerd = Model.execute_query(query, connection)
        if is_titles_registerd:
            Model.commit(connection)
        else:
            Model.rollback(connection)
        return is_titles_registerd

    @staticmethod
    def register_company_activity(company_id, activity, connection):
        """ call functions, one for forming an insert query, and another for executing query
        :param company_id: company Identification in database
        :param activity: values in type of List
        :param connection: connection to the server
        :return: true if query execution is successful, or False conversely
        """
        activities = activity['activity'].split(',')
        table = 'activities'
        columns = ' (name, company_id)'
        query = Registry.insert_from_list(company_id, activities, table, columns)
        is_activities_registered = Model.execute_query(query, connection)
        if is_activities_registered:
            Model.commit(connection)
        else:
            Model.rollback(connection)
        return is_activities_registered

    @staticmethod
    def insert_from_list_dict(data, company_id, table):
        len_one_dict = len(data[0])
        length = len(data)
        i = 0
        query = 'INSERT INTO ' + table
        values = ' VALUES '
        columns = ' ('
        cls = data[0].keys()
        for index, key in enumerate(cls):
            columns += key + ','
            if index == len_one_dict - 1:
                columns += 'company_id)'
        for dic in data:
            i = i + 1
            for index, (k, v) in enumerate(dic.items()):
                if index == 0:
                    values += '('
                values += '"' + str(v) + '",'
                if index == len_one_dict - 1:
                    values += '"'+str(company_id)+'")'
                    if i != length:
                        values += ','
        query += columns + values
        return query

    @staticmethod
    def register_station(company_id, station, connection):
        table = 'stations'
        stations = station['stations']
        query = Registry.insert_from_list_dict(stations, company_id, table)
        is_stations_register = Model.execute_query(query, connection)
        if is_stations_register:
            Model.commit(connection)
        else:
            Model.rollback(connection)
        return is_stations_register
