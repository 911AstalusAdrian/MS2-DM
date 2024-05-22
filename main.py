import numpy as np
import pandas as pd
from api_work import race_results
# import pandas as pd
from quali_performance import QualiPerformance


def extras():
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
    print(results_list)


if __name__ == '__main__':
    quali_csv = './csv_files/qualifying.csv'
    quali_data = QualiPerformance(quali_csv)

    # print(quali_data.get_top20())
