import requests
# results_api = f'http://ergast.com/api/f1/{season}/{race}/results.json'


def get_races_number(season):
    seasons_api = f'https://ergast.com/api/f1/{season}.json'
    response = requests.get(seasons_api)
    response = response.json()
    return response['MRData']['total']


def get_race_name(season, race):
    result_api = f'http://ergast.com/api/f1/{season}/{race}/results.json'
    response = requests.get(result_api)
    response = response.json()
    return response['MRData']['RaceTable']['Races'][0]['raceName']


def get_race_winner(season, race):
    result_api = f'http://ergast.com/api/f1/{season}/{race}/results.json'
    response = requests.get(result_api)
    response = response.json()
    results = response['MRData']['RaceTable']['Races'][0]['Results']
    return results[0]['Driver']['driverId']