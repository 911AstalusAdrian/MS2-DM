import numpy as np
import pandas as pd
import re


def convert_to_millis(laptime):
    if isinstance(laptime, str):
        match = re.match(r'(\d+):(\d+)\.(\d+)', laptime)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            milliseconds = int(match.group(3))
            total_milliseconds = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
            return total_milliseconds
    return np.nan


def apply_percentages(group):
    min_best_q = group['best_q'].min()

    group['qual_percentage'] = (group['best_q'] * 100) / min_best_q
    return group


class QualiPerformance():
    def __init__(self, filename):
        self.__fn = filename
        self.__df = self.__read_filename()
        self.__final_df = None
        self.__format_df()

    def __read_filename(self):
        df = pd.read_csv(self.__fn)
        df.replace('\\N', np.nan, inplace=True)
        return df

    def __format_df(self):
        # Convert qualifying times to milliseconds where applicable
        self.__df['q1_millis'] = self.__df['q1'].apply(convert_to_millis)
        self.__df['q2_millis'] = self.__df['q2'].apply(convert_to_millis)
        self.__df['q3_millis'] = self.__df['q3'].apply(convert_to_millis)

        # Set the best qualifying time for each entry
        self.__df['best_q'] = self.__df[['q1_millis', 'q2_millis', 'q3_millis']].min(axis=1)

        # Drop irrelevant columns
        self.__df = self.__df.drop(['constructorId', 'number', 'q1', 'q2', 'q3', 'q1_millis', 'q2_millis', 'q3_millis'],
                                   axis=1)

        # Group data by raceId and compute qualifying percentages per race, then ungroup
        grouped = (self.__df
                   .groupby('raceId', as_index=False)
                   .apply(apply_percentages))
        self.__df = grouped.reset_index().drop(['level_0', 'level_1'], axis=1)

        # Group data by driverId and compute the mean qualifying percentage and average position for each driver
        self.__final_df = self.__df.groupby('driverId').agg({
            'qual_percentage': 'mean',
            'position': 'mean'
        }).reset_index()
        self.__final_df.columns = ['driverId', 'avg_qual', 'avg_pos']

        rows_to_drop = self.__final_df[self.__final_df['avg_qual'] > 120].index
        self.__final_df = self.__final_df.drop(rows_to_drop)

    def get_final_df(self):
        return self.__final_df

    def get_top20(self):
        return self.__df.head(20)
