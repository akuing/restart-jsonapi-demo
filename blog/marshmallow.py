from __future__ import absolute_import

from six import with_metaclass
import marshmallow as ma
from marshmallow_jsonapi import SchemaOpts, Schema, fields


class SqlaSchemaMeta(type(Schema)):
    """Metaclass for the SqlaSchema class. Registers all subclasses of SqlaSchema
    into ``SqlaSchema._class_registry``, which is a dictionary mapping subclass
    names to schema classes.
    """

    def __new__(mcs, name, bases, attrs):
        klass = super(SqlaSchemaMeta, mcs).__new__(mcs, name, bases, attrs)
        if name != 'SqlaSchema':
            SqlaSchema._class_registry[name] = klass
        return klass


class SqlaSchemaOpts(SchemaOpts):

    def __init__(self, meta):
        super(SqlaSchemaOpts, self).__init__(meta)
        self.model_class = getattr(meta, 'model_class', None)
        self.session = getattr(meta, 'session', None)


class SqlaSchema(with_metaclass(SqlaSchemaMeta, Schema)):

    _class_registry = {}

    OPTIONS_CLASS = SqlaSchemaOpts

    def __init__(self, *args, **kwargs):
        include_relationships = kwargs.pop('include_relationships', [])
        super(SqlaSchema, self).__init__(*args, **kwargs)
        self.include_relationships = include_relationships

    def validate_extra_args(self):
        errors = []
        for field_name in self.include_relationships:
            if '.' in field_name:
                errors.append({
                    'source': {'parameter': 'include'},
                    'detail': 'Multi-part relationship path is unsupported.'
                })

            rel = self.declared_fields.get(field_name)
            if not isinstance(rel, fields.BaseRelationship):
                errors.append({
                    'source': {'parameter': 'include'},
                    'detail': ('The resource does not have a relationship '
                               'path named `{}`.').format(field_name)
                })
        return errors

    @ma.post_dump(pass_many=True, pass_original=True)
    def format_json_api_response(self, data, many, original_data):
        """Pre-dump hoook that formats serialized data as a top-level JSON API object.

        See: http://jsonapi.org/format/#document-top-level
        """
        ret = self.format_items(data, many)
        ret = self.wrap_response(ret, many)
        if self.include_relationships:
            ret = self.format_related_items(ret, original_data)
        return ret

    def format_related_items(self, ret, original_data):
        items = []
        for field_name in self.include_relationships:
            rel = self.declared_fields.get(field_name)
            value = getattr(original_data, field_name)
            d = rel.schema_class().dump(value).data
            items.append(d['data'])
        ret['included'] = items
        return ret


class SqlaRelationship(fields.Relationship):

    def __init__(self, schema_class=None, **kwargs):
        super(SqlaRelationship, self).__init__(**kwargs)
        self.schema_class_name = schema_class

    @property
    def schema_class(self):
        if self.schema_class_name is None:
            return None
        return SqlaSchema._class_registry[self.schema_class_name]

    @property
    def session(self):
        if self.schema_class is None:
            return None
        return self.schema_class.opts.session

    @property
    def model_class(self):
        if self.schema_class is None:
            return None
        return self.schema_class.opts.model_class

    def extract_value(self, data):
        value = super(SqlaRelationship, self).extract_value(data)
        import pdb; pdb.set_trace()
        if self.sesion is not None and self.model_class is not None:
            value = self.session.query(self.model_class).get(value)
        return value