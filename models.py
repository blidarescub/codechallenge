from security import decrypt_w, encrypt_w, import_key

from sqlalchemy import (
    # Boolean,
    Column,
    # DateTime,
    Integer,
    String
)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    'mysql+mysqlconnector://root:test@db:3306/words_db',
    echo=True
)

Base = declarative_base()
publickey = import_key('public_key.pem')


class Word(Base):
    __tablename__ = 'words'
    hash = Column(String(length=256), primary_key=True)
    value = Column(String(length=2048), nullable=False)
    frequency = Column(Integer(), nullable=False)

    def __repr__(self):
        return "<Word('%s'):%i>" % (
            decrypt_w(self.username, publickey),
            self.frequency
        )


class Url(Base):
    __tablename__ = 'urls'
    hash = Column(String(length=256), primary_key=True)
    url = Column(String(length=256), primary_key=True)
    sentiment = Column(String(length=256), nullable=False)

    def __repr__(self):
        return "<Url('%s'): %s>" % (self.url, self.sentiment)


words_table = Word.__table__
urls_table = Url.__table__
