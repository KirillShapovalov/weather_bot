from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy_mixins import AllFeaturesMixin

Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


postgres_params = dict(
    host='localhost',
    port=5405,
    dbname='weather_db',
    user='postgres',
    password='postgres',
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
