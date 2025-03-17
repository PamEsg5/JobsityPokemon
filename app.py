from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

import api.views as view

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemonAPI.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pokemon(db.Model):
    """
    Model for Pokemon data
    """
    api_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    moves = db.Column(db.JSON)
    types = db.Column(db.JSON)
    sprites = db.Column(db.JSON)
    abilities = db.Column(db.JSON)
    stats = db.Column(db.JSON)

with app.app_context():
    db.create_all()

migrate = Migrate()
migrate.init_app(app,db)


@app.route("/create_pokemon/<poke_name>")
def create_pokemon(poke_name):
    """
    Endpoint that stores the pokemon data into de db
    :param poke_name: <pokemon name>
    :return: pokemon_name, status
    """
    name = poke_name
    pokemon =  view.PokemonView()
    poke_data = pokemon.create(name)
    new_pokemon = Pokemon(api_id=poke_data['id'],
                          name=poke_data['name'],
                          weight=poke_data['weight'],
                          height=poke_data['height'],
                          moves=poke_data['moves'],
                          types=poke_data['types'],
                          sprites=poke_data['sprites'],
                          abilities=poke_data['abilities'],
                          stats=poke_data['stats'])
    try:
        db.session.add(new_pokemon)
        db.session.commit()
        return Response(f'Pokemon {new_pokemon.name} created',status=200)
    except Exception as e:
        return Response(f'Error while creating a new pokemon {str(e)}',
                        status=400)

@app.route("/display_pokemon/<poke_name>")
def display_pokemon(poke_name):
    """
    Endpoint that shows a single pokemon data
    :param poke_name: <pokemon name>
    :return: pokemon object
    """
    name = poke_name
    try:
        pokemon_data = Pokemon.query.filter_by(name=name.lower()).first()
        pokemon = {'id':pokemon_data.api_id,
                   'name': pokemon_data.name,
                   'weight': pokemon_data.weight,
                   'height': pokemon_data.height,
                   'moves': pokemon_data.moves,
                   'types': pokemon_data.types,
                   'sprites': pokemon_data.types,
                   'abilities': pokemon_data.abilities,
                   'stats': pokemon_data.stats
                 }
        return Response(json.dumps(pokemon),status=200)
    except Exception as e:
        return Response(f'Error while fetching pokemon{str(e)}',
                        status=400)

@app.route("/display_all_pokemons/")
def display_all():
    """
    Endpoint that shows all stored pokemons
    :return: Pokemons data object
    """
    pokemons = []
    try:
        pokemon_data = Pokemon.query.all()
        for pokemon in pokemon_data:
            pokemons.append({'id':pokemon.api_id,
                             'name': pokemon.name,
                             'weight': pokemon.weight,
                             'height': pokemon.height,
                             'moves': pokemon.moves,
                             'types': pokemon.types,
                             'sprites': pokemon.types,
                             'abilities': pokemon.abilities,
                             'stats': pokemon.stats
                             })
        return Response(json.dumps(pokemons), status=200)
    except Exception as e:
        return Response(f'Error while fetching pokemons{str(e)}',
                        status=400)

if __name__ == '__main__':
    app.run(debug=True)