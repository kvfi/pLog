import datetime
import os

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from plog import lmanager, db


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.EmailField(unique=True)
    username = db.StringField(default=True)
    password = db.StringField(default=True)
    is_active = db.BooleanField(default=True)
    is_admin = db.BooleanField(default=False)
    timestamp = db.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.email

    def generate_auth_token(self, exp=600):
        s = Serializer(os.environ.get('SECRET_KEY'), expires_in=exp)
        return s.dump({'id': self.username})

    def verify_auth_token(token):
        s = Serializer(os.environ.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        u = data['id']
        return u


@lmanager.user_loader
def user_loader(user_id):
    return User.objects(pk=user_id).first()
