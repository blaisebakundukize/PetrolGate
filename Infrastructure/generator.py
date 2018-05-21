import uuid


class Generator(object):

    def __init__(self, first_numbers, last_numbers):
        self.first = first_numbers
        self.last = last_numbers

    @staticmethod
    def generate_account(fist_number, last_number):
        """
        :return: account number
        """
        return str(fist_number) + str(last_number)

    @staticmethod
    def generate_identity(number_of_ids):
        """ generate identifications
        :param number_of_ids: number of identities
        :return: return a list of identifications
        """
        ids = []
        for i in xrange(number_of_ids):
            new_uuid = 'petrol_stations_db.UUID_TO_BIN("'+str(uuid.uuid1())+'")'
            ids.append(new_uuid)
        return ids
