from constants import SIS
from modelfactory import ModelFactory

class Manager:
    def __init__(self, engine, schema, opts={}):
        self.model = ModelFactory(schema)
        self.schema = schema
        self.engine = engine
        self.idField = opts.get(SIS.OPT_ID_FIELD, SIS.FIELD_NAME)
        self.type = opts.get(SIS.OPT_TYPE, self.model.modelName)
        self.authEnabled = opts.get(SIS.OPT_USE_AUTH, SIS.DEFAULT_OPT_USE_AUTH)

    def getReferences(self):
        # return a list of fields that are objects within the schema
        pass

    def validate(self, obj, toUpdate, options):
        # return a string if validation fails
        pass

    def applyUpdate(self, doc, updateObj):
        # set the json data to the schema doc
        doc.set(updateObj)
        return doc

    async def objectRemoved(self, obj):
        # async method that removes the object
        await self.model.delete(obj)

    def _getDefaultOptions(self, options={}):
        if 'version' not in options:
            options['version'] = "v1.1"
        return options

    def _getFindOptions(self, options={}):
        result = {}
        if not options:
            return result
        for opt in SIS.QUERY_PARAMETER_OPTIONS:
            if opt in options:
                result[opt] = options[opt]
        return result

    async def getSingleByCondition(self, condition, name, options={}):
        result = None
        try:
            result = await self.model.findOne(condition, null, self._getFindOptions(options))
        except Exception as err:
            return SIS.ERR_INTERNAL(err)
        if not result:
            return SIS.ERR_NOT_FOUND(self.type, name)

    async def getById(self, id, options={}):
        q = {self.idField: id}
        return await self.getSingleByCondition(q, id, options)

    async def getAll(self, condition, options, fields):
        return await self.model.find(condition, fields, self._getFindOptions(options))

    async def count(self, condition):
        return await self.model.count(condition)

    def getPopulateFields(self, schemaManager, subList):
        pass

         
        


        
