import hashlib

from flask_restful import Resource, reqparse

from plog.util.mongo import MongoDB

server = MongoDB.getInstance()

_users = server.client.plog.users

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}


class UsersApi(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rate', type=int, required=True, help='Rate cannot be converted')
        parser.add_argument('name')
        args = parser.parse_args()
        print(args)
        u = []
        users = _users.find()
        for user in users:
            user_ = {'id': hashlib.md5(str(user['_id']).encode()).hexdigest(), 'email': user['email']}
            u.append(user_)
        return u
