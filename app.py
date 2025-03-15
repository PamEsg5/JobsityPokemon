from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from api.views import PokemonView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemonAPI.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

migrate = Migrate()
migrate.init_app(app,db)


@app.route("/create_pokemon/<poke_name>")
def create_pokemon(poke_name):
    name = poke_name
    pokemon =  PokemonView()
    poke_data = pokemon.create(name)
    print(poke_data)

if __name__ == '__main__':
    app.run(debug=True)