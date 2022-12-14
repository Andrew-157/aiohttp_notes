from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import Table, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("tag", Integer, ForeignKey("tags.id", ondelete="CASCADE"))
)


class Note(Base):

    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())
    description = Column(String(150), nullable=False)
    done = Column(Boolean, default=False)
    tags = relationship(
        "Tag", secondary=note_m2m_tag, backref="notes", passive_deletes=True)


class Tag(Base):

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)


async def pg_context(app):
    conf = app['config']['postgres']
    url_db = f"postgresql://{conf['user']}:{conf['password']}@{conf['host']}/{conf['database']}"
    engine = create_engine(url_db)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    app['session_db'] = session
    yield
    app['session_db'].close()
