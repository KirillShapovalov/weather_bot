from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy_mixins import AllFeaturesMixin
import os

Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


postgres_params = dict(
    host=os.getenv('PG_HOST', 'localhost'),
    port=int(os.getenv('PG_PORT', 5405)),
    dbname=os.getenv('PG_DATABASE', 'weather_db'),
    user=os.getenv('PG_USERNAME', 'postgres'),
    password=os.getenv('PG_PASSWORD', 'postgres'),
)


def get_session():
    engine = create_engine('postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(dbname)s' % postgres_params)
    return Session(engine)


def set_session():
    engine = create_engine('postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(dbname)s' % postgres_params)
    db_session = scoped_session(
        sessionmaker(autocommit=True, autoflush=False, bind=engine)
    )
    BaseModel.set_session(db_session)
    Base.query = db_session.query_property()
    Base.metadata.create_all(engine)
