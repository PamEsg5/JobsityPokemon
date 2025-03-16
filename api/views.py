import requests

class PokemonView():

    def create(self, name):
        """
        Method that gets pokemon data from an external API
        :param name: pokemon name
        :return: pokemon data as dict
        """
        try:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
        except Exception as e:
            raise f"Error while connecting to Pokemon external API {str(e)}"

        data = response.json()
        data = self._create_pokemon_data(data)
        return data

    def _create_pokemon_data(self, data):
        """
        Method that formats received data
        :param data: api data
        :return: pokemon data as dict
        """

        pokemon_moves = self._parse_moves_data(data['moves'])
        pokemon_types = self._parse_types_data(data['types'])
        pokemon_sprites = self._parse_sprites_data(data['sprites'])
        pokemon_abilities = self._parse_abilities_data(data['abilities'])
        pokemon_stats = self._parse_stats_data(data['stats'])

        pokemon_data = {'id': data['id'],
                        'name': data['name'],
                        'weight': data['weight'],
                        'height': data['height'],
                        'types': pokemon_types,
                        'moves': pokemon_moves,
                        'sprites': pokemon_sprites,
                        'abilities': pokemon_abilities,
                        'stats': pokemon_stats}
        return pokemon_data

    def _parse_types_data(self, types_data):
        """
        Method that formats types data
        :param types_data:
        :return: formated dict
        """
        types = []
        for ptype in types_data:
            types.append(ptype['type']['name'])
        return types

    def _parse_moves_data(self, moves_data):
        """
        Method that formats moves data
        :param moves_data: dict
        :return: formated dict
        """
        moves = []
        for move in moves_data:
            moves.append(move['move']['name'])
        return moves

    def _parse_sprites_data(self, sprites_data):
        """
        Method that formats sprites data
        :param sprites_data: dict
        :return: formated dict
        """
        sprites  = []
        if sprites_data['back_default']:
            sprites.append(sprites_data['back_default'])
            sprites.append(sprites_data['back_shiny'])
            sprites.append(sprites_data['front_default'])
            sprites.append(sprites_data['front_shiny'])
        elif sprites_data['back_female']:
            sprites.append(sprites_data['back_female'])
            sprites.append(sprites_data['back_shiny_female'])
            sprites.append(sprites_data['front_female'])
            sprites.append(sprites_data['front_shiny_female'])

        return sprites

    def _parse_abilities_data(self, abilities_data):
        """
        Metdod that formats abilities data
        :param abilities_data: dict
        :return: formated dict
        """
        abilities = {}
        for ability in abilities_data:
            descriptions = self._get_abilities_description(ability['ability']['url'])
            abilities.update({ability['ability']['name']:descriptions})
        return abilities

    def _get_abilities_description(self, ab_url):
        """
        Method that formats abilities description, need to fetch the
        data from an external API
        :param ab_url: url for fetching data
        :return: formated dict
        """
        resp = requests.get(ab_url)
        effects_data = resp.json()
        effects = []
        effect_change_data = effects_data['effect_changes']
        for effect_change in effect_change_data:
            for eff in effect_change['effect_entries']:
                if eff['language']['name'] == 'en':
                    effects.append(eff['effect'])

        for effect_entry in effects_data['effect_entries']:
            if effect_entry['language']['name'] == 'en':
                effects.append(effect_entry['short_effect'])
        return effects

    def _parse_stats_data(self, stats_data):
        """
        Method that formats stats data
        :param stats_data: dict
        :return: formated dict
        """
        stats = []
        for stat in stats_data:
            stats.append(stat['stat']['name'])
        return stats









