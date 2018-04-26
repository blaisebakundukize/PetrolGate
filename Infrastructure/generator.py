

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
