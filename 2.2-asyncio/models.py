from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///star_wars.db')
Session = sessionmaker(bind=engine)

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)

def create_database():
    engine = create_engine('sqlite:///star_wars.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == '__main__':
    create_database()