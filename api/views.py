import requests


class PokemonView():

    def create(self, name):
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
        data = response.json()
        self._create_pokemon_data(data)

    def _create_pokemon_data(self, data):

        pokemon_types = self._parse_types_data(data['types'])
        pokemon_moves = self._parse_moves_data(data['moves'])

        pokemon_data = {'id': data['id'],
                        'name': data['name'],
                        'weight': data['weight'],
                        'height': data['height'],
                        'types': pokemon_types,
                        'moves': pokemon_moves}
        print(pokemon_data)

    def _parse_types_data(self, types_data):
        types = []
        for ptype in types_data:
            types.append(ptype['type']['name'])
        return types

    def _parse_moves_data(self, moves_data):
        moves = []
        for move in moves_data:
            moves.append(move['move']['name'])
        return moves






