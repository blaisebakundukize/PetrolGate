import hashlib


class HardGuess(object):
    def __init__(self, data):
        self.data = data

    @staticmethod
    def secure_data(data):
        d = hashlib.sha256(data)
        return d.hexdigest()

    @staticmethod
    def check_password(password):
        digits = 0
        caps = 0
        length = len(password)
        passed = True
        if length < 8:
           return False
        for ch in password:
           if ch.isdigit():
               digits += 1
           elif ch.isupper():
               caps += 1
        if digits <= 0:
            passed = False
        if caps <= 0:
            passed = False
        if passed:
            return True
        else:
            return False

    @staticmethod
    def validate_password(password, confirm_password=None):
        length = len(password)
        must_length = 4
        passed = True
        if confirm_password is not None and password != confirm_password:
            passed = False
        if length != must_length:
            passed = False
        if password.isdigit() is False:
            passed = False
        if passed:
            return True
        else:
            return False











































































