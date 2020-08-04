import requests


class PokeApiAdapter:
    def __init__(self):
        self.base_url = 'https://pokeapi.co/api/v2'

    def url_generator(self, endpoint=None, name_or_id=None, offset=None, limit=None):
        """
        This method generates url with given params. It would return base url if no params is given.
        :param endpoint: takes endpoint(not required)
        :param name_or_id: takes name or id to specify request(not required)
        :param offset: takes integer to specify slice of data we need(not required)
        :param limit: takes integer to specify number of items in response(not required)
        :return: url
        """
        if not endpoint:
            return self.base_url
        name_or_id = f'{name_or_id}/' if name_or_id else ''
        offset_limit = ''
        if all((offset, limit)):
            offset_limit = f'?offset={offset}&limit={limit}'
        elif offset:
            offset_limit = f'?offset={offset}'
        elif limit:
            offset_limit = f'?limit={limit}'

        url = f'{self.base_url}/{endpoint}/{name_or_id}{offset_limit}'
        return url

    def if_pokemon_exist(self, name):
        """
        This method check if pokemon presented in PokeAPI.
        :param name: takes name of pokemon
        :return: True if Pokemon presented or False if it is no evidence of Pokemon presence
        """
        url = self.url_generator(endpoint='pokemon', name_or_id=name)
        response = requests.get(url)
        if response.status_code == 200:
            return True
        return False

    def get_pokemon_data(self, name):
        """
        This method gets Pokemon data
        :param name: takes name of pokemon
        :return: dict with pokemon data or False if this Pokemon not presented in PokeAPI
        """
        url = self.url_generator(endpoint='pokemon', name_or_id=name)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return False

    @staticmethod
    def extract_pokemon_data(json_data):
        """
        This method extract Pokemon data from json API response
        :param json_data: takes dict with info about pokemon from API
        :return: tuple with required data for one Pokemon
        """
        name = json_data.get('name', 'unknown')
        height = json_data.get('height', 0)
        weight = json_data.get('weight', 0)
        image = json_data.get('sprites', dict()).get('front_default')

        stats_list_of_dicts = json_data.get('stats', [{i: None} for i in range(6)])

        speed = stats_list_of_dicts[0].get('base_stat', 0)
        special_defence = stats_list_of_dicts[1].get('base_stat', 0)
        special_attack = stats_list_of_dicts[2].get('base_stat', 0)
        defence = stats_list_of_dicts[3].get('base_stat', 0)
        attack = stats_list_of_dicts[4].get('base_stat', 0)
        hp = stats_list_of_dicts[5].get('base_stat', 0)

        types_list_of_dicts = json_data.get('types', [{i: None} for i in range(2)])

        type_1 = types_list_of_dicts[0].get('type', dict()).get('name', 'unknown')
        type_2 = types_list_of_dicts[1].get('type', dict()).get('name') if len(types_list_of_dicts) == 2 else None

        api_id = json_data.get('id', 0)

        pokemon_data = (name, height, weight, image, speed, special_defence,
                        special_attack, defence, attack, hp, type_1, type_2, api_id)
        return pokemon_data
