from pymongo import MongoClient


class MongoDB:
    instance = None

    class MongoDBHelper:

        def __call__(self, *args, **kw):
            if MongoDB.instance is None:
                obj = MongoDB()
                MongoDB.instance = obj
            return MongoDB.instance

    getInstance = MongoDBHelper()

    def __init__(self):
        if MongoDB.instance is not None:
            raise (RuntimeError, 'Only one instance of TestSingleton is allowed!')

        self.host = '51.15.42.140'
        self.username = 'plog'
        self.password = 'pL0g24121992!'
        self.database = 'plog'
        self.client = MongoClient(self.host, username=self.username, password=self.password, authSource=self.database)
        self.users = self.client.plog.users

    def __repr__(self):
        return '<%s.%s object at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )

    def get_emails(self):
        m = []
        for u in self.users:
            m.append(u['email'])
        return m
