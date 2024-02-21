from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    ___tablename__ = 'hero'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    #relating to other powers
    superpowers = db.relationship('Power', secondary="hero_powers", backref='superhero')
    
    def __repr__(self):
        return f"{self.id}: {self.name} is {self.super_name}"




class HeroPower(db.Model):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #relationships to other tables
    hero = db.relationship('Hero', backref=db.backref('hero_powers', cascade='all, delete-orphan'))
    power = db.relationship('Power', backref=db.backref('hero_powers', cascade='all, delete-orphan'))

    @validates('strength')
    def validating_the_strength(self, key, value):
        accepted_strengths = ['Strong', 'Weak', 'Average']
        if value not in accepted_strengths:
            raise ValueError("Strength type is not accepted")
        return value

    def __repr__(self):
        return f"{self.id}: Strength is {self.strength}, Hero Id is {self.hero_id}, Power Id is {self.power_id}"





class Power(db.Model):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #relationships with other tables
    superheroes = db.relationship('Hero', secondary="hero_powers", backref='powers')

    @validates('description')
    def validating_the_description(self, key, value):
        if not value:
            raise ValueError("Please provide a description")
        if len(value) < 20:
            raise ValueError("Description provided must be at least 20 characters long")
        return value

    def __repr__(self):
        return f"{self.id}: {self.name}: {self.description}"