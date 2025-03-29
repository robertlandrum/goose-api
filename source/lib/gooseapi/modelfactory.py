from typing import List, Optional
from odmantic import Model, Field, EmbeddedModel
from bson import ObjectId

basics = {
    "String": str,
    "Boolean": bool,
    "Number": int,
    "Mixed": ObjectId,
    "ObjectId": ObjectId
}

def ModelFactory(app, schema, baseclass=Model):

    fields = {}
    annotations = {}
    if 'definition' in schema:
        recurse(schema['definition'], fields, annotations, 0, baseclass=Model)

def recurse(mydef, fields, annotations, depth):
    if depth > 5:
        return None

    if type(mydef) is dict:
        for key, value in mydef.items():
            fieldname = key
            schemafieldname = key
            fielddef = value
            if type(value) is str:
                fielddef = {"type": value}
            elif type(value) is list:
                fielddef = {"type": value}
            elif type(value) is dict and 'type' not in value:
                # nested dict - EmbeddedModel

            set_field_annotation(app, fieldname, fielddef, annotations)

                
            isrequired = False
            isunique = False
            hasindex = False
            isenum = False
            hasmatch = False
            if key.startswith('_'):
                fieldname = key.ltrim('_')

                # simple field def
                set_field_annotation(value, fieldname, annotations)

            if typeof(value) is dict:
                # could be a subobject or just complex field definition
                if 'type' in value:
                    # assume field definition, not dict
                    set_field_annotations(value['type'], fieldname, annotations)
            if type(value) is list:
                if value[0] in basics:
                    annotations[fieldname] = List(basics[value[0])


                
    if type(mydef) is list:

def set_field_annotation(app, fieldname, fielddef, annotations):
    isrequired = 'required' in fielddef and fielddef['required'] is True

    if type(fielddef['type']) is list:
        annotations[fieldname] = List[basics[fielddef['type'][0]]]
    elif fielddef['type'] == 'ObjectId' and 'ref' in fielddef:
        model = app.get_model(fielddef['ref'])
        annotations[fieldname] = model if isrequired else Optional[model]
    else:
        annotations[fieldname] = basics[fielddef['type']] if isrequired else Optional[basics[fielddef['type']]]
