from api_work import race_results

if __name__ == '__main__':

    for season in range(2020, 2023):
        races = int(race_results.get_races_number(season))
        print(f'{season} - {races}')
        for race in range(1, races + 1):
            race_name = race_results.get_race_name(season, race)
            race_date = race_results.get_race_winner(season, race)
            print(f'\t{race} - {race_name}')
            print(f'\t\t{race_date}')

