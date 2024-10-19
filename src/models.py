import os
import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    profile_picture = Column(String(250))
    bio = Column(String(250))
    
    posts = relationship('Post', back_populates='user')
    comentarios = relationship('Comentario', back_populates='user')
    seguidores = relationship('Seguidor', foreign_keys='Seguidor.follower_id')
    seguidos = relationship('Seguidor', foreign_keys='Seguidor.followed_id')

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False)
    caption = Column(String(250))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('usuario.id'))
    
    user = relationship('Usuario', back_populates='posts')
    comentarios = relationship('Comentario', back_populates='post')

class Comentario(Base):
    __tablename__ = 'comentario'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('usuario.id'))
    
    post = relationship('Post', back_populates='comentarios')
    user = relationship('Usuario', back_populates='comentarios')

class Seguidor(Base):
    __tablename__ = 'seguidor'
    
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('usuario.id'))
    followed_id = Column(Integer, ForeignKey('usuario.id'))

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
