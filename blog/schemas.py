from __future__ import absolute_import

from marshmallow_jsonapi import fields

from .marshmallow import SqlaSchema, SqlaRelationship
from .models import session, Article, Person, Tag, Comment


class ArticleSchema(SqlaSchema):
    id = fields.Integer(as_string=True)
    title = fields.Str()

    author = SqlaRelationship(
        schema_class='PersonSchema',
        self_url='/articles/{article_id}/relationships/author',
        self_url_kwargs={'article_id': '<id>'},
        related_url='/articles/{article_id}/author',
        related_url_kwargs={'article_id': '<id>'},
        include_data=True,
        type_='people'
    )

    tags = SqlaRelationship(
        schema_class='TagSchema',
        self_url='/articles/{article_id}/relationships/tags',
        self_url_kwargs={'article_id': '<id>'},
        related_url='/articles/{article_id}/tags',
        related_url_kwargs={'article_id': '<id>'},
        include_data=True,
        many=True,
        type_='tags'
    )

    comments = SqlaRelationship(
        schema_class='CommentSchema',
        self_url='/articles/{article_id}/relationships/comments',
        self_url_kwargs={'article_id': '<id>'},
        related_url='/articles/{article_id}/comments',
        related_url_kwargs={'article_id': '<id>'},
        include_data=True,
        many=True,
        type_='comments'
    )

    class Meta:
        type_ = 'articles'
        strict = True
        self_url = '/articles/{id}'
        self_url_kwargs = {'id': '<id>'}
        self_url_many = '/articles',

        session = session
        model_class = Article


class PersonSchema(SqlaSchema):
    id = fields.Integer(as_string=True)
    first_name = fields.Str()
    last_name = fields.Str()

    class Meta:
        type_ = 'people'
        strict = True
        self_url = '/people/{id}'
        self_url_kwargs = {'id': '<id>'}
        self_url_many = '/people'

        session = session
        model_class = Person


class TagSchema(SqlaSchema):
    id = fields.Integer(as_string=True)
    name = fields.Str()

    class Meta:
        type_ = 'tags'
        strict = True
        self_url = '/tags/{id}'
        self_url_kwargs = {'id': '<id>'}
        self_url_many = '/tags'

        session = session
        model_class = Tag


class CommentSchema(SqlaSchema):
    id = fields.Integer(as_string=True)
    name = fields.Str()

    author = SqlaRelationship(
        schema_class='PersonSchema',
        self_url='/comments/{comment_id}/relationships/author',
        self_url_kwargs={'comment_id': '<id>'},
        related_url='/comments/{comment_id}/author',
        related_url_kwargs={'comment_id': '<id>'},
        include_data=True,
        type_='people'
    )

    class Meta:
        type_ = 'comments'
        strict = True
        self_url = '/comments/{id}'
        self_url_kwargs = {'id': '<id>'}
        self_url_many = '/comments'

        session = session
        model_class = Comment
