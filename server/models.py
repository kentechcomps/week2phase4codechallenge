from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from wsgiref import validate
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from sqlalchemy.orm import validates 

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model , SerializerMixin):
    __tablename__ = 'hero'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    super_name = db.Column(db.String)
    power = db.relationship('Heropower', backref='hero')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    serialize_rules = ('-Heropower.hero',)
class Power(db.Model, SerializerMixin):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String)
    hero = db.relationship('Heropower', backref='power')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('description')
    def validatedescription(self , key , description):
        if len(description) < 20:
            raise ValueError("Must be at least 20 characters long.")
        
        return description

    
    serialize_rules = ('-Heropower.power',)
class Heropower(db.Model , SerializerMixin):
    __tablename__ = 'Heropower'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('strength')
    def validatestrenght(self , key ,strength):
        validstrength = ['Strong' , 'Weak' , 'Average']
        if strength not in validstrength:
            raise ValueError("Invalid strenth value.Strenght must be 'Strong" , 'Weak' , 'Average')
        return strength
    
    serialize_rules = ('-hero.Heropower', '-power.Heropower',)

