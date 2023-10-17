
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Time

Base = declarative_base()

# tabelki z pobi

class Klient(Base):
    __tablename__ = 'klient'
    id = Column(Integer, primary_key=True)
    imie_nazwisko = Column(String)
    wiek = Column(Integer)

class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    tytul = Column(String)
    gatunek = Column(String)
    czas_trwania = Column(Integer)
    data_seansu = Column(String),
    godzina_seansu = Column(Time)
    cena = Column(Float)

class Sala(Base):
    __tablename__ = 'sala'
    id = Column(Integer, primary_key=True)
    numer = Column(Integer)
    nazwa = Column(String)
    pojemnosc = Column(Integer)

class Siedzenie(Base):
    __tablename__ = 'siedzenie'
    id = Column(Integer, primary_key=True)
    rzad = Column(Integer)
    miejsce = Column(Integer)
    sala_id = Column(Integer, ForeignKey('sala.id'))
    sala = relationship("Sala", back_populates="siedzenia")

Sala.siedzenia = relationship("Siedzenie", order_by=Siedzenie.id, back_populates="sala")

class Jedzenie(Base):
    __tablename__ = 'jedzenie'
    id = Column(Integer, primary_key=True)
    nazwa = Column(String)
    typ = Column(String)
    rozmiar = Column(String)
    cena = Column(Float)

class Bilet(Base):
    __tablename__ = 'bilet'
    id = Column(Integer, primary_key=True)
    klient_id = Column(Integer, ForeignKey('klient.id'))
    siedzenie_id = Column(Integer, ForeignKey('siedzenie.id'))
    film_id = Column(Integer, ForeignKey('film.id'))
    klient = relationship("Klient", back_populates="bilety")
    siedzenie = relationship("Siedzenie")
    film = relationship("Film")

Klient.bilety = relationship("Bilet", order_by=Bilet.id, back_populates="klient")

# dziedziczenie

class BiletNormalny(Bilet):
    __tablename__ = 'bilet_normalny'
    id = Column(Integer, ForeignKey('bilet.id'), primary_key=True)
    cena_dodatkowa = Column(Float)
    
    __mapper_args__ = {
        'polymorphic_identity':'bilet_normalny',
    }

class BiletUlgowy(Bilet):
    __tablename__ = 'bilet_ulgowy'
    id = Column(Integer, ForeignKey('bilet.id'), primary_key=True)
    procent_ulg = Column(Float)
    
    __mapper_args__ = {
        'polymorphic_identity':'bilet_ulgowy',
    }

# tworzenie bazy sqlite
engine = create_engine('sqlite:///kino.db')

# tworzenie tabel
Base.metadata.create_all(engine)
