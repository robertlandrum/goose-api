from constants import SIS
import re

metaDef = {
    SIS.FIELD_CREATED_AT: { "type": "Number" },
    SIS.FIELD_UPDATED_AT: { "type": "Number" },
    SIS.FIELD_CREATED_BY: { "type": "String" }, 
    SIS.FIELD_UPDATED_BY: { "type": "String" }, 
    SIS.FIELD_LOCKED: { "type": "Boolean", required: True, "default": False },
    SIS.FIELD_IMMUTABLE: { "type": "Boolean", "default": False },
    SIS.FIELD_TAGS: { "type": ["String"], "index": True },
    SIS.FIELD_SIS_VERSION: "String"
}

schemas = [
    # sis_schemas
    {
        "name": SIS.SCHEMA_SCHEMAS,
        "definition": {
            "name": { "type": "String", "required": True, "unique": True, "match": re.compile(/^[a-z0-9_]+$/) },
            "description": { "type": "String" },
            "definition": { "type": {}, "required": True },
            "locked_fields": { "type": ["String"] },
            "track_history": { "type": "Boolean", "default": True },
            "is_open": { "type": "Boolean", "default": False },
            "id_field": { "type": "String", "default": "_id" },
            "is_public": { "type": "Boolean", "default": False },
            "any_owner_can_modify": { "type": "Boolean", "default": False },
            "_sis": {
                "owner": { "type": ["String"], "required": True },
                "_references": ["String"]
            }
        }
    },
    # sis_hooks
    {
        "name": SIS.SCHEMA_HOOKS,
        "definition": {
            "name": { "type": "String", "required": True, "unique": True, "match": re.compile(/^[a-z0-9_]+$/) },
            "target": {
                "type": {
                    "url": { "type": "String", "required": True },
                    "action": { "type": "String", "required": True, "enum": ["GET", "POST", "PUT"] },
                },
                "required": True
            }
            "retry_count": { "type": "Number", "min": 0, "max", 20, "default": 0 },
            "retry_delay": { "type": "Number", "min": 1, "max", 60, "default": 1 },
            "events": { "type": [{ "type": "String", "enum": SIS.EVENTS_ENUM }], "required": True },
            "entity_type": { "type": "String", "required": True },
            "_sis": {
                "owner": { "type": ["String"], "required": True }
            }
        }
    },
    # sis_hiera
    {
        "name": SIS.SCHEMA_HIERA,
        "definition": {
            "name": { "type": "String", "required": True, "unique": True, "match": re.compile(/^[a-z0-9_]+$/) },
            "hieradata": { "type": {}, "required": True },
            "_sis": {
                "owner": { "type": ["String"], "required": True }
            }
        }
    },
    # sis_commits
    {
        "name": SIS.SCHEMA_COMMITS,
        "definition": {
            "type": { "required": True, "type": "String" },
            "entity_id": { "required": True, "type": "String" },
            "entity_oid": { "required": True, "type": "String" },
            "action": { "required": True, "type": "String", "enum": SIS.EVENTS_ENUM },
            "commit_data": "Mixed",
            "date_modified": { "type": "Number", "index": True },
            "modified_by": "String"
        }
    },
    # sis_users
    {
        "name": SIS.SCHEMA_USERS,
        "definition": {
            "name": { "type": "String", "required": True, "unique": True, "match": re.compile(/^[a-z0-9_\-]+$/) },
            "email": { "type": "String", "required": True, "match": re.compile(/^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/) },
            "verified": { "type": "Boolean", "default": False },
            "super_user": { "type": "Boolean", "default": False },
            "pw": { "type": "String" },
            "roles": { "type": {}, "default": {} }
        }
    },
    # sis_tokens
    {
        "name": SIS.SCHEMA_TOKENS,
        "definition": {
            "name": { "type": "String", "unique": True },
            "desc": "String",
            "expires": { "type": "Date", "expires": 0 },
            "username": { "type": "String", "required": True },
        }
    },
    # sis_scripts
    {
        "name": SIS.SCHEMA_SCRIPTS,
        "definition": {
            "name": { "type": "String", "required": True, "unique": True, "match": re.compile(/^[a-z0-9_]+$/) },
            "description": "String",
            "script_type": { "type": "String", "required": True, "enum": ["application/javascript"] },
            "script": { "type": "String", "required": True, "code": True, "code_type_field": "script_type" },
            "_sis": {
                "owner": { "type": ["String"], "required": True },
            }
        }
    }
]

        

                        

