import requests


# results_api = f'http://ergast.com/api/f1/{season}/{race}/results.json'

def get_races_number(season):
    seasons_api = f'https://ergast.com/api/f1/{season}.json'
    response = requests.get(seasons_api)
    response = response.json()
    return response['MRData']['total']


def get_race_name_API(season, race):
    result_api = f'http://ergast.com/api/f1/{season}/{race}/results.json'
    response = requests.get(result_api)
    response = response.json()
    return response['MRData']['RaceTable']['Races'][0]['raceName']


def get_driver_time(race_place_data):
    if 'Time' in race_place_data:
        return race_place_data['Time']['time']
    else:
        return '0'


def get_results_json(season, race):
    result_api = f'http://ergast.com/api/f1/{season}/{race}/results.json'
    response = requests.get(result_api)
    results = response.json()['MRData']['RaceTable']['Races'][0]['Results']
    return results


def get_driver_result(driver_info):
    driver_data = {
        'position': driver_info['position'],
        'name': driver_info['Driver']['givenName'] + ' ' + driver_info['Driver']['familyName'],
        'constructor': driver_info['Constructor']['name'],
        'time': get_driver_time(driver_info),
        'lapsCompleted': driver_info['laps'],
        'startingPosition': driver_info['grid'],
        'points': driver_info['points'],
        'status': driver_info['status']}
    return driver_data


def get_race_results(season, race, race_id, results_list):

    results = get_results_json(season, race)
    for driver in results:
        final_data = {'raceId': race_id}
        driver_result = get_driver_result(driver)
        final_data.update(driver_result)
        results_list.append(final_data)
