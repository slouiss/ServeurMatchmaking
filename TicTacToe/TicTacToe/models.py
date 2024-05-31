from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Queue(Base):
    __tablename__ = 'queue'

    id = Column(Integer, primary_key=True)
    ip = Column(String(255))
    port = Column(Integer)
    pseudo = Column(String(255))
    entry_date = Column(DateTime)

class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    player1_ip = Column(String(255))
    player1_port = Column(Integer)
    player2_ip = Column(String(255))
    player2_port = Column(Integer)
    board_state = Column(String(9))  # Utiliser une chaîne pour l'état du jeu
    is_finished = Column(Boolean, default=False)
    winner = Column(String(255))

class Turn(Base):
    __tablename__ = 'turn'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer)
    player = Column(String(1))
    move_position = Column(Integer)
