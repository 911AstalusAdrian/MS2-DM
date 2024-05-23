from api_work import race_results
from quali_performance import QualiPerformance
from sklearn.cluster import KMeans
import pandas as pd


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


def merge_df(quali_df, drivers_df):
    drivers_selected = drivers_df[['driverId', 'driverRef', 'code']]
    return pd.merge(quali_df, drivers_selected, on='driverId', how='inner')


if __name__ == '__main__':
    quali_csv = './csv_files/qualifying.csv'
    drivers_csv = './csv_files/drivers.csv'

    clusters = KMeans(n_clusters=3, random_state=42)

    quali_data = QualiPerformance(quali_csv)
    driver_data = pd.read_csv(drivers_csv)
    final_data = merge_df(quali_data.get_final_df(), driver_data)

    final_data['cluster'] = clusters.fit_predict(final_data['avg_qual'])

    print(final_data)
    # print(quali_data.get_top20())
