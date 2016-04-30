from __future__ import absolute_import

from restart import status, exceptions
from restart.resource import Resource
from restart.parsers import JSONParser
from restart.renderers import JSONRenderer
from restart.utils import make_location_header


class JSONAPIParser(JSONParser):
    content_type = 'application/vnd.api+json'


class JSONAPIRenderer(JSONRenderer):
    content_type = 'application/vnd.api+json'
    format_suffix = 'jsonapi'


class JSONAPIResource(Resource):
    parser_classes = (JSONAPIParser,)
    renderer_classes = (JSONAPIRenderer,)

    schema_class = None

    @property
    def session(self):
        return self.schema_class.opts.session

    @property
    def model_class(self):
        return self.schema_class.opts.model_class

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.HTTPException):
            # Always render `HTTPException` messages into JSON API
            self.renderer_classes = (JSONAPIRenderer,)

            headers = dict(exc.get_headers(self.request.environ))
            rv = (exc.description, exc.code, headers)
            return rv
        else:
            self.log_exception(exc)
            raise

    def get_pk(self, pk):
        try:
            return int(pk)
        except ValueError:
            raise exceptions.NotFound()

    def get_row(self, pk):
        row = self.session.query(self.model_class).get(self.get_pk(pk))
        if not row:
            raise exceptions.NotFound()
        return row

    def get_include_args(self, args):
        include_args_str = args.get('include')
        include_args = include_args_str.split(',') if include_args_str else []
        return include_args

    def index(self, request):
        collection = self.session.query(self.model_class).all()
        return self.schema_class().dump(collection, many=True).data

    def create(self, request):
        data = self.schema_class().load(request.data).data
        # Do not support creating a resource with a client-generated ID
        if 'id' in data:
            errors = [{
                'source': {'pointer': '/data/id'},
                'detail': 'Creating a resource with a client-generated ID is unsupported.'
            }]
            return exceptions.Forbidden({'errors': errors})

        # Save to db
        entity = self.model_class(**data)
        self.session.add(entity)
        self.session.commit()

        result = self.schema_class().dump(entity).data
        headers = {'Location': make_location_header(request, entity.id)}
        return result, status.HTTP_201_CREATED, headers

    def read(self, request, pk):
        include_args = self.get_include_args(request.args)
        entity = self.get_row(pk)
        schema = self.schema_class(include_relationships=include_args)
        errors = schema.validate_extra_args()
        if errors:
            raise exceptions.Forbidden({'errors': errors})
        result = schema.dump(entity).data
        return result

    def update(self, request, pk):
        entity = self.get_row(pk)
        data = self.schema_class().load(request.data).data
        import pdb; pdb.set_trace()

    def delete(self, request, pk):
        entity = self.get_row(pk)
        self.session.delete(entity)
        self.session.commit()
        return '', status.HTTP_204_NO_CONTENT