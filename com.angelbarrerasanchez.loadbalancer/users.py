import hashlib
import uuid
import redistore
from pymongo import MongoClient

mongouser = "user"
mongopass = "mypass"
mongohost = "localhost"
mongoport = "27017"
mongodbname = "mydatabase"
mongocollectionname = "users"
mongouri = "mongodb://%s:%s@%s:%s/%s" % (mongouser, mongopass, mongohost, mongoport, mongodbname)

mongo = MongoClient(mongouri)
mongodb = mongo[mongodbname]
mongocollection = mongodb[mongocollectionname]

users = list()


class User(object):
    def __init__(self, email, password):
        self.id = email
        self.email = email
        self.password = password
        self.apps = list()

    def __str__(self):
        return "User(email='%s')" % (self.email)

    def to_dict(self):
        user_dict = dict()
        user_dict['id'] = self.id
        user_dict['email'] = self.email
        user_dict['password'] = self.password
        user_dict['apps'] = self.apps
        return user_dict

    @staticmethod
    def from_dict(user_dict):
        user = User(email=user_dict['email'], password=user_dict['password'])
        user.apps = user_dict['apps']
        user.id = user_dict['id']
        return user

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
        self.apps.append(appname)

    def remove_app_to_user(self, appname):
        self.apps.remove(appname)
        redistore.delete_app(appname)


def register_user(user_json):
    if not user_exists(user_json['email']):
        user = User(user_json['email'], User.hash_password(user_json['password']))
        mongocollection.insert_one(user.to_dict())
        return True
    else:
        return False


def remove_user(user_json):
    cursor = mongocollection.find({"email": user_json['email']})
    if cursor.count() == 1:
        user = cursor.next()
        if user['email'] == user_json['email'] and User.check_password(user['password'], user_json['password']):
            for app in user['apps']:
                redistore.delete_app(app)

            mongocollection.remove(user)
            cursor.close()
            return True
    cursor.close()
    return False


def authenticate(email, password):
    cursor = mongocollection.find({"email": email})
    if cursor.count() == 1:
        user = cursor.next()
        if user['email'] == email and User.check_password(user['password'], password):
            cursor.close()
            return User.from_dict(user)
    cursor.close()
    return None


def identity(user_json):
    if user_exists(user_json['identity']):
        return user_json['identity']
    else:
        return None


def user_exists(email):
    cursor = mongocollection.find({"email": email})
    if cursor.count() > 0:
        cursor.close()
        return True
    else:
        cursor.close()
        return False