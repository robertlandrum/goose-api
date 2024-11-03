from sisschemas import schemas
from usermanager import UserManager
from tokenmanager import TokenManager

class SchemaManager(Manager):
    def __init__(self, pymongo, opts):
        self.pymongo = pymongo
        self.entitySchemaToUpdateTime = {}
        self.models = {}
        for schema in schemas:
            self.models[schema] = self.getEntityModel(schema, True)

        self.model = self.getSisModel(SIS.SCHEMA_SCHEMAS)
        # call parent module init method ?
        if self.authEnabled:
            self.auth = {}
            self.auth[SIS.SCHEMA_USERS] = UserManager(pymongo, opts)
            self.tokenFetcher = TokenManager(pymongo, opts)

        self.managerCache = {}

    def validate(self, modelObj, toUpdate, options):
        pass

    def invalidateSchema(self, name):
        del self.models[name]
        del self.entitySchemaToUpdateTime[name]

        
