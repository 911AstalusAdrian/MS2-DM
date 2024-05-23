from api_work import race_results
from quali_performance import QualiPerformance
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import plotly.express as px


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
    scaler = MinMaxScaler()

    quali_data = QualiPerformance(quali_csv)
    driver_data = pd.read_csv(drivers_csv)
    final_data = merge_df(quali_data.get_final_df(), driver_data)

    # final_data['qual_normalized'] = scaler.fit_transform(final_data[['avg_qual']])
    final_data['cluster'] = clusters.fit_predict(final_data[['avg_qual', 'avg_pos']])
    final_data['cluster'] = final_data['cluster'].astype(str)
    # print(final_data)

    labels = {
        0: 'Poor Qualifier',
        1: 'Great Qualifier',
        2: 'Average Qualifier'
    }

    fig = px.scatter(
        final_data,
        x='avg_pos',
        y='avg_qual',
        color='cluster',
        hover_data=['driverRef', 'avg_qual', 'avg_pos'],
        labels={
            'avg_pos': 'Average qualifying position',
            'avg_qual': 'Average qualifying percentage'
        },
        title='Driver clustering based on average quali position and quali percentage',
    )
    for i, label in labels.items():
        fig.for_each_trace(lambda trace: trace.update(name=label) if trace.name == str(i) else ())

    fig.show()

    # plt.figure(figsize=(10, 6))
    # colors = ['red', 'green', 'orange']
    # for cluster in range(3):
    #     clustered_data = final_data[final_data['cluster'] == cluster]
    #     plt.scatter(clustered_data['avg_pos'], clustered_data['avg_qual'],
    #                 label=f'Cluster {cluster}', color=colors[cluster])
    #
    # plt.xlabel('Average quali position')
    # plt.ylabel('Average quali percentage')
    # plt.title('')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # print(final_data)
    # print(quali_data.get_top20())
