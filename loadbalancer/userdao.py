import hashlib
import uuid
import appserversdao
import constants
from pymongo import MongoClient

mongo = MongoClient(constants.MONGO_URI)
mongodb = mongo[constants.MONGO_DATABASE]
mongocollection = mongodb[constants.MONGO_USERS_COLLECTION]

users = list()


class User(object):
    def __init__(self, email, password):
        self.id = email
        self.email = email
        self.password = password

    def __str__(self):
        return "User(email='%s')" % (self.email)

    def to_dict(self):
        user_dict = dict()
        user_dict['id'] = self.id
        user_dict['email'] = self.email
        user_dict['password'] = self.password
        return user_dict

    @staticmethod
    def from_dict(user_dict):
        user = User(email=user_dict['email'], password=user_dict['password'])
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


def register_user(email, password):
    if not user_exists(email):
        user = User(email, User.hash_password(password))
        mongocollection.insert_one(user.to_dict())
        return True
    else:
        return False


def remove_user(email, password):
    cursor = mongocollection.find({"email": email})
    if cursor.count() == 1:
        user = cursor.next()
        if user['email'] == email and User.check_password(user['password'], password):
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