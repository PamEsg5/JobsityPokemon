from sqlalchemy import ForeignKey

from app import db

class Pokemon(db.Model):
    api_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    moves: db.Column(db.List)
    types: db.Column(db.List)

class Abilities(db.Model):
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.api_id'), nullable=False)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))

class Sprites(db.Model):
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.api_id'), nullable=False)
    back = db.Column(db.String(200))
    back_shiny = db.Column(db.String(200))
    front = db.Column(db.String(200))
    front_shiny = db.Column(db.String(200))
    female = db.Column(db.Boolean)

class Stats(db.Model):
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.api_id'), nullable=False)
    name = db.Column(db.String(50))
    characteristics: db.Column(db.List)