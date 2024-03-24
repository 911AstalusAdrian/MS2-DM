from api_work import race_results

if __name__ == '__main__':

    race_id = 1
    results_list = []
    for season in range(2015, 2023):
        races = int(race_results.get_races_number(season))
        for race in range(1, races + 1):
            race_name = race_results.get_race_name_API(season, race)
            print(f'{season} - {race_name}')
            race_results.get_race_results(season, race, race_id, results_list)
            race_id += 1

    for result in results_list:
        print(result)
    # print(results_list)