import hashlib
import uuid
import redistore

users = list()


class User(object):
    def __init__(self, email, password):
        self.id = email
        self.email = email
        self.password = password
        self.apps = set()

    def __str__(self):
        return "User(email='%s')" % (self.email)

    @staticmethod
    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    def add_app_to_user(self, appname):
        self.apps.add(appname)

    def remove_app_to_user(self, appname):
        self.apps.remove(appname)
        redistore.delete_app(appname)


def register_user(user_json):
    user = User(user_json['email'], User.hash_password(user_json['password']))
    users.append(user)
    return True


def remove_user(user_json):
    for user in users:
        if user.email == user_json['email'] and User.check_password(user.password, user_json['password']):
            users.remove(user)
            return True
        else:
            return False


def authenticate(email, password):
    for user in users:
        if user.email == email and User.check_password(user.password, password):
            return user
        else:
            return None


def identity(user_json):
    if user_exists(user_json['identity']):
        return user_json['identity']
    else:
        return None


def user_exists(email):
    return [element for element in users if element.email == email]