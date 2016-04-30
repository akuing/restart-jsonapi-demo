from __future__ import absolute_import

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = sa.create_engine('sqlite:////Users/russellluo/Projects/restart-jsonapi-demo/blog/sqlite.db', echo=True)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


article_tags = sa.Table('article_tags', Base.metadata,
    sa.Column('article_id', sa.ForeignKey('articles.id'), primary_key=True),
    sa.Column('tag_id', sa.ForeignKey('tags.id'), primary_key=True),
)


class Article(Base):
    __tablename__ = 'articles'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('people.id'))

    author = relationship('Person')
    tags = relationship('Tag', secondary=article_tags)
    comments = relationship('Comment', order_by='Comment.id')


class Person(Base):
    __tablename__ = 'people'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)


class Comment(Base):
    __tablename__ = 'comments'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    article_id = sa.Column(sa.Integer, sa.ForeignKey('articles.id'))
    author_id = sa.Column(sa.Integer, sa.ForeignKey('people.id'))

    author = relationship('Person')


class Tag(Base):
    __tablename__ = 'tags'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


Base.metadata.create_all(engine)
