import json

class SIS:
    FIELD_LOCKED = "locked"
    FIELD_IMMUTABLE = "immutable"
    FIELD_OWNER = "owner"
    FIELD_TAGS = "tags"
    FIELD_SIS_META = "_sis"
    FIELD_SIS_VERSION = "_version"
    CURRENT_VERSION = "v1.1"
    FIELD_VERS = "_v"

    LOGGER = None
    EVENT_INSERT = "insert"
    EVENT_UPDATE = "update"
    EVENT_DELETE = "delete"
    EVENTS_ENUM = ["insert", "update", "delete"]

    METHOD_PUT = "PUT"
    METHOD_POST = "POST"
    METHOD_GET = "GET"
    METHOD_DELETE = "DELETE"

    METHODS_TO_EVENT = {
        "PUT": "update",
        "POST": "insert",
        "DELETE": "delete"
    }

    FIELD_ID = "_id"
    FIELD_NAME = "name"
    FIELD_EXPIRES = "expires"
    FIELD_TOKEN = "token"
    FIELD_DESC = "desc"
    FIELD_ROLES = "roles"
    FIELD_PW = "pw"
    FIELD_SUPERUSER = "super_user"
    FIELD_CREATOR = "creator"
    FIELD_EMAIL = "email"
    FIELD_USERNAME = "username"
    FIELD_TOKEN_USER = "sis_token_user"
    FIELD_MODIFIED_BY = "modified_by"
    FIELD_VERIFIED = "verified"
    FIELD_LOCKED_FIELDS = "locked_fields"
    FIELD_TRACK_HISTORY = "track_history"
    FIELD_DESCRIPTION = "description"
    FIELD_IS_OPEN = "is_open"
    FIELD_ID_FIELD = "id_field"
    FIELD_ANY_ADMIN_MOD = "any_owner_can_modify"
    FIELD_IS_PUBLIC = "is_public"
    FIELD_ENTITY_COUNT = "entity_count"

    FIELD_REFERENCES = "_references"
    FIELD_TRANSACTION_ID = "_trans_id"
    FIELD_CREATED_AT = "_created_at"
    FIELD_UPDATED_AT = "_updated_at"
    FIELD_CREATED_BY = "_created_by"
    FIELD_UPDATED_BY = "_updated_by"

    MUTABLE_META_FIELDS = [
        SIS.FIELD_TAGS,
        SIS.FIELD_IMMUTABLE,
        SIS.FIELD_OWNER,
        SIS.FIELD_LOCKED
    ]

    SCHEMA_SCHEMAS = "sis_schemas"
    SCHEMA_HOOKS = "sis_hooks"
    SCHEMA_HIERA = "sis_hiera"
    SCHEMA_COMMITS = "sis_commits"
    SCHEMA_USERS = "sis_users"
    SCHEMA_TOKENS = "sis_tokens"
    SCHEMA_SCRIPTS = "sis_scripts"

    AUTH_EXPIRATION_TIME = 60 * 60 * 8 # 8 hours
    AUTH_TYPE_SIS = "sis"
    AUTH_TYPE_LDAP = "ldap"
    AUTH_TYPES = ["sis", "ldap"]

    OPT_SCHEMA_MGR = "schema_manager"
    OPT_LOG_COMMTS = "log_commits"
    OPT_FIRE_HOOKS = "fire_hooks"
    OPT_READONLY = "readonly"
    OPT_ID_FIELD = "id_field"
    OPT_TYPE = "type"
    OPT_USE_AUTH = "auth"
    OPT_AUTH_CONFIG = "auth_config"

    SUPPORTED_VERSIONS = ["v1.1"]
    
    ROLE_USER = "user"
    ROLE_ADMIN = "admin"

    PERMISSION_ADMIN = "admin"
    PERMISSION_USER = "user"
    PERMISSION_USER_ALL_GROUPS = "all_groups"
    PERMISSION_NONE = "none"

    DEFAULT_OPT_USE_AUTH = True

    EP_READY = "ready"
    EP_REQ = "request"
    EP_ERROR = "error"
    EP_DONE = "done"

    MAX_BODY_SIZE_BYTES = 10 * 1024 * 1024
    MAX_RESULTS = 10000

    HEADER_TOTAL_COUNT = "x-total-count"
    HEADER_AUTH_TOKEN = "x-auth-token"

    QUERY_PARAMETER_OPTIONS = ['skip', 'limit', 'sort', 'lean', 'populate', 'read']

    @staticmethod
    def ERR_NOT_FOUND(type, id):
        return JSONResponse({"error": f"{type} {id} does not exist", "code": 1000}, status_code=404)

    @staticmethod
    def ERR_BAD_REQ(msg):
        return JSONResponse({"error": f"Bad request: {msg}", "code": 1001}, status_code=400)

    @staticmethod
    def ERR_INTERNAL(msg):
        if msg is None:
            return None
        if isinstance(msg, 'ValidationError'):
            return JSONResponse({"error": f"Invalid data: {msg}", "code": 1003}, status_code=400)

        return JSONResponse({"error": f"Internal error {msg}", "code": 1002}, status_code=500)

    @staticmethod
    def ERR_INTERNALOR_NOT_FOUND(err, type, id, result):
        if err is not None:
            if isinstance(err, 'CastError'):
                return SIS.ERROR_NOT_FOUND(type, id)
            return SIS.ERR_INTERNAL(err)
        else:
            return SIS.ERR_NOT_FOUND(type, id)

    @staticmethod
    def ERR_BAD_CREDS(msg):
        if not isinstance(msg, str):
            msg = json.dumps(msg)
        return JSONResponse({"error": f"Unauthorized. {msg}", "code": 1004}, status_code=401)

    @staticmethod
    def UTIL_MERGE_SHALLOW(obj, partial):
        for k,v in partial.items():
            if k not in obj:
                obj[k] = v

    @staticmethod
    def UTIL_ARRAYS_EQUAL(a, b):
        if a == b:
            return True
        if a is None or b is None:
            return False
        if len(a) != len(b):
            return False

    @staticmethod
    def UTIL_ROLES_EQUAL(a, b):
        aroles = a.roles
        broles = b.roles
        if aroles == broles:
            return True
        if aroles is None or broles is None:
            return False
        arolenames = aroles.keys().sort()
        brolenames = broles.keys().sort()
        if SIS.UTIL_ARRAYS_EQUAL(arolenames, brolenames):
            return True

    @staticmethod
    def UTIL_VALIDATE_ROLES(obj, isUser):
        if isUser:
            if obj[SIS.FIELD_SUPERUSER]:
                return None
        if not SIS.FIELD_ROLES in obj:
            return "roles are missing."

        roles = obj[SIS.FIELD_ROLES]

        try:
            keys = roles.keys()
            if len(keys) == 0:
                return None
            for k in keys:
                if roles[k] != SIS.ROLE_USER and roles[k] != SIS.ROLE_ADMIN:
                    return f"invalid role specified: {roles[k]}"
        except Exception as ex:
            return "roles must be a non empty object"
        return None

    @staticmethod
    def UTIL_ENSURE_ROLE_SUBSET(roles, subset, adminOnly):
        if roles is None or len(roles) == 0:
            return False
        if subset is None or len(subset) == 0:
            return True

        for k in subset:
            if k not in roles:
                return False
            masterRole = roles[k]
            subRole = subset[k]
            if adminOnly:
                if masterRole != SIS.ROLE_ADMIN:
                    return False
            else:
                if masterRole == SIS.ROLE_USER and subRole == SIS.ROLE_ADMIN:
                    return False
        return True

    @staticmethod
    def UTIL_GET_OID_PATHS(schema):
        paths = []
        return paths

    @staticmethod
    def ENSURE_SIS_META(obj):
        if obj is None:
            return obj
        obj[SIS.FIELD_SIS_META] = obj.get(SIS.FIELD_SIS_META, {})
        sisMeta = obj[FIELD_SIS_META]
        if SIS.FIELD_SIS_VERSION not in sisMeta:
            sisMeta[SIS.FIELD_SIS_VERSION] = SIS.CURRENT_VERSION
        return obj

    @staticmethod
    def UTIL_SET_DEFAUL_ARRAY(obj, path):
        paths = path.split('.')
        last = paths.pop()
        while len(paths) > 0:
            p = paths.pop(0)
            obj = obj[p]
            if not obj:
                return
            if not obj[last]
                obj[last] = []


