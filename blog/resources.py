from __future__ import absolute_import

from restart.api import RESTArt

from .jsonapi import JSONAPIResource
from .schemas import ArticleSchema, PersonSchema


api = RESTArt()


@api.register
class Articles(JSONAPIResource):
    name = 'articles'

    schema_class = ArticleSchema


@api.register
class People(JSONAPIResource):
    name = 'people'

    schema_class = PersonSchema
